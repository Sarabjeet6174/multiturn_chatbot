from flask import Flask, render_template, request, jsonify,session
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI
from openai._exceptions import AuthenticationError, RateLimitError
import sqlite3
import os
load_dotenv()
app=Flask(__name__)
CORS(app)
app.secret_key = "123"
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=openai_api_key,
)
def get_data_from_db():
    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()
    c.execute("SELECT text FROM data LIMIT 1")
    result = c.fetchone()
    conn.close()
    return result[0] if result else ""
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/ask",methods=["POST"])
def ask():
    try:
        print("📥 Received request to /ask")
        user_input = request.json["message"]
        print("🧾 Received JSON:", request.json)

        context = get_data_from_db()
        print("📚 Context from DB:", context[:60])

        if "chat_history" not in session:
            print("🆕 Initializing chat history")
            session["chat_history"] = [
                {"role": "system", "content": f"Use this context to answer user questions: {context}"}
            ]

        print("➕ Appending user message to chat history")
        session["chat_history"].append({"role": "user", "content": user_input})

        print("🧠 Sending to LLM...")
        response = client.chat.completions.create(
            model="openai/gpt-4.1",
            messages=session["chat_history"],
            max_tokens=500
        )

        bot_reply = response.choices[0].message.content
        # print("🤖 Bot reply:", bot_reply)

        session["chat_history"].append({"role": "assistant", "content": bot_reply})

        return jsonify({"reply": bot_reply})

    except AuthenticationError:
        print("❌ Invalid API key.")
        return jsonify({"error": "Invalid API key."}), 401
    except RateLimitError:
        print("❌ Rate limit exceeded.")
        return jsonify({"error": "Rate limit exceeded. Please try again later."}), 429
    except Exception as e:
        print("❌ Internal server error:", e)
        return jsonify({"error": str(e)}), 500

# def ask():
#     try:
#         user_input = request.json["message"]
#         print("Received JSON:", request.json)

#         context = get_data_from_db() 
#         # Initialize if not already set
#         if "chat_history" not in session:
#             session["chat_history"] = [
#                 {"role": "system", "content": f"Use this context to answer user questions: {context}"}
#             ]

#     # Add user's question
#         session["chat_history"].append({"role": "user", "content": user_input})

#         # Call the model with full history
#         response = client.chat.completions.create(
#             model="openai/gpt-4.1",
#             messages=session["chat_history"],
#             max_tokens=5000
#         )

#         # Append assistant's reply
#         bot_reply = response.choices[0].message.content
#         session["chat_history"].append({"role": "assistant", "content": bot_reply})
        
#         print(bot_reply)

#         return jsonify({"reply": bot_reply})
            

    # except AuthenticationError:
    #     return jsonify({"error": "Invalid API key."}), 401
    # except RateLimitError:
    #     return jsonify({"error": "Rate limit exceeded. Please try again later."}), 429
    # except Exception as e:
    #     print("❌ Internal server error:", e)
    #     return jsonify({"error": str(e)}), 500
            

if __name__=="__main__":
      app.run(debug="True")