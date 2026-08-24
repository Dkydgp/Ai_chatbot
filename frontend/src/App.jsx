import { useState } from "react";
import "./App.css";
import ReactMarkdown from "react-markdown";

const API_URL = "http://localhost:8000";

function App() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const [feedbackOpen, setFeedbackOpen] = useState(false);
  const [selectedRating, setSelectedRating] = useState(0);
  const [reason, setReason] = useState("");
  const [comment, setComment] = useState("");
  const [feedbackSubmitted, setFeedbackSubmitted] = useState(false);

  const [lastQuestion, setLastQuestion] = useState("");
  const [lastAnswer, setLastAnswer] = useState("");

  const sendMessage = async () => {
    if (!message.trim() || loading) return;

    const userMessage = message.trim();

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: userMessage,
      },
    ]);

    setMessage("");
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: userMessage,
        }),
      });

      if (!response.ok) {
        throw new Error("Chat request failed");
      }

      const data = await response.json();

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.response,
        },
      ]);

      setLastQuestion(userMessage);
      setLastAnswer(data.response);

      setFeedbackOpen(true);
      setSelectedRating(0);
      setReason("");
      setComment("");
      setFeedbackSubmitted(false);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "Sorry, I couldn't connect to the Cafe De Flora assistant. Please try again.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const submitFeedback = async () => {
    if (selectedRating === 0) return;

    if (selectedRating <= 2 && !reason) {
      alert("Please select a reason for the low rating.");
      return;
    }

    try {
      const response = await fetch(`${API_URL}/feedback`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: lastQuestion,
          bot_response: lastAnswer,
          rating: selectedRating,
          reason: selectedRating <= 2 ? reason : null,
          comment: comment || null,
        }),
      });

      if (!response.ok) {
        throw new Error("Feedback request failed");
      }

      const data = await response.json();

      if (data.success) {
        setFeedbackSubmitted(true);

        setTimeout(() => {
          setFeedbackOpen(false);
        }, 2000);
      }
    } catch (error) {
      alert("Unable to submit feedback. Please try again.");
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      sendMessage();
    }
  };

  return (
    <div className="app">

      {/* HEADER */}
      <header className="header">
        <div>
          <h1>Cafe De Flora</h1>
          <p>AI Customer Assistant</p>
        </div>

        <div className="status">
          <span className="status-dot"></span>
          Online
        </div>
      </header>


      {/* MAIN CHAT */}
      <main className="chat-container">

        {/* WELCOME SCREEN */}
        {messages.length === 0 && (
          <div className="welcome">

            <div className="welcome-icon">
              ☕
            </div>

            <h2>
              Welcome to Cafe De Flora
            </h2>

            <p>
              Ask me about our menu, prices, vegetarian options,
              location, online ordering and more.
            </p>

            <div className="suggestions">

              <button
                onClick={() =>
                  setMessage(
                    "What vegetarian pizzas do you have?"
                  )
                }
              >
                Vegetarian pizzas
              </button>

              <button
                onClick={() =>
                  setMessage(
                    "What is the cheapest item on the menu?"
                  )
                }
              >
                Cheapest item
              </button>

              <button
                onClick={() =>
                  setMessage(
                    "How can I order online?"
                  )
                }
              >
                Order online
              </button>

            </div>

          </div>
        )}


        {/* MESSAGES */}
        <div className="messages">

          {messages.map((msg, index) => (

            <div
              key={index}
              className={`message-row ${msg.role}`}
            >

              <div
                className={`message ${msg.role}`}
              >

                {/* USER MESSAGE */}
                {msg.role === "user" && (
                  <div>
                    {msg.content}
                  </div>
                )}


                {/* AI MESSAGE */}
                {msg.role === "assistant" && (
                  <ReactMarkdown
                    components={{
                      a: ({
                        node,
                        ...props
                      }) => (
                        <a
                          {...props}
                          target="_blank"
                          rel="noopener noreferrer"
                        />
                      ),
                    }}
                  >
                    {msg.content}
                  </ReactMarkdown>
                )}

              </div>

            </div>

          ))}


          {/* LOADING */}
          {loading && (
            <div className="message-row assistant">

              <div className="message assistant typing">
                Thinking...
              </div>

            </div>
          )}

        </div>


        {/* FEEDBACK */}
        {feedbackOpen && lastAnswer && (

          <div className="feedback-box">

            {!feedbackSubmitted ? (

              <>

                <h3>
                  How helpful was this answer?
                </h3>


                {/* STARS */}
                <div className="stars">

                  {[1, 2, 3, 4, 5].map(
                    (star) => (

                      <button
                        key={star}
                        className={
                          star <= selectedRating
                            ? "star selected"
                            : "star"
                        }
                        onClick={() =>
                          setSelectedRating(star)
                        }
                        aria-label={`${star} star rating`}
                      >
                        ★
                      </button>

                    )
                  )}

                </div>


                {/* LOW RATING */}
                {selectedRating > 0 &&
                  selectedRating <= 2 && (

                    <div className="low-rating">

                      <p>
                        We're sorry the answer
                        wasn't helpful.
                      </p>

                      <select
                        value={reason}
                        onChange={(e) =>
                          setReason(e.target.value)
                        }
                      >

                        <option value="">
                          Select a reason
                        </option>

                        <option value="Incorrect information">
                          Incorrect information
                        </option>

                        <option value="Didn't answer my question">
                          Didn't answer my question
                        </option>

                        <option value="Information was missing">
                          Information was missing
                        </option>

                        <option value="Other">
                          Other
                        </option>

                      </select>


                      <textarea
                        placeholder="Tell us more (optional)"
                        value={comment}
                        onChange={(e) =>
                          setComment(e.target.value)
                        }
                      />

                    </div>

                  )}


                {/* NORMAL FEEDBACK */}
                {selectedRating >= 3 && (

                  <textarea
                    className="feedback-comment"
                    placeholder="Tell us more (optional)"
                    value={comment}
                    onChange={(e) =>
                      setComment(e.target.value)
                    }
                  />

                )}


                {/* SUBMIT */}
                {selectedRating > 0 && (

                  <button
                    className="submit-feedback"
                    onClick={submitFeedback}
                  >
                    Submit Feedback
                  </button>

                )}

              </>

            ) : (

              <div className="thank-you">
                ❤️ Thank you for your feedback!
              </div>

            )}

          </div>

        )}


        {/* INPUT */}
        <div className="input-area">

          <input
            type="text"
            placeholder="Ask something about Cafe De Flora..."
            value={message}
            onChange={(e) =>
              setMessage(e.target.value)
            }
            onKeyDown={handleKeyDown}
          />

          <button
            className="send-button"
            onClick={sendMessage}
            disabled={loading}
          >
            {loading ? "..." : "Send"}
          </button>

        </div>

      </main>


      {/* FOOTER */}
      <footer>
        Cafe De Flora AI Assistant
      </footer>

    </div>
  );
}

export default App;