import { useState } from "react";
import { apiRequest, ApiError } from "../api/client.js";

export default function AuthForm({ onAuthenticated }) {
  const [mode, setMode] = useState("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const isRegistering = mode === "register";

  async function submit(event) {
    event.preventDefault();
    setError("");
    setSuccess("");
    setSubmitting(true);
    const cleanEmail = email.trim().toLowerCase();
    try {
      if (isRegistering) {
        await apiRequest("/auth/register", {
          method: "POST",
          body: JSON.stringify({ email: cleanEmail, password }),
        });
        // Auto-login immediately upon registration
        try {
          const user = await apiRequest("/auth/login", {
            method: "POST",
            body: JSON.stringify({ email: cleanEmail, password }),
          });
          onAuthenticated(user);
          return;
        } catch {
          // If auto-login fails, prompt to sign in
          setEmail(cleanEmail);
          setMode("login");
          setPassword("");
          setSuccess("Your account is ready. Sign in with your 6-digit PIN.");
        }
      } else {
        const user = await apiRequest("/auth/login", {
          method: "POST",
          body: JSON.stringify({ email: cleanEmail, password }),
        });
        onAuthenticated(user);
      }
    } catch (requestError) {
      if (isRegistering && requestError instanceof ApiError && requestError.status === 409) {
        setMode("login");
        setPassword("");
        setSuccess("This email already has an account. Sign in with your PIN or password.");
      } else {
        setError(requestError.message);
      }
    } finally {
      setSubmitting(false);
    }
  }

  function changeMode(nextMode) {
    setMode(nextMode);
    setError("");
    setSuccess("");
    setPassword("");
    setShowPassword(false);
  }

  return (
    <main className="auth-layout">
      <section className="auth-story" aria-label="About Daymark">
        <a className="brand brand-light" href="/" aria-label="Daymark home">
          <span className="brand-icon" aria-hidden="true">d</span>
          <span>daymark</span>
        </a>
        <div className="story-copy">
          <p className="eyebrow eyebrow-light">MAKE ROOM FOR WHAT MATTERS</p>
          <h1>A calmer way to get things <span>done.</span></h1>
          <p>Gather your plans in one clear place, and give your day a little more breathing room.</p>
        </div>
        <div className="story-note">
          <span className="note-icon" aria-hidden="true">✳</span>
          <span>Progress, not pressure.</span>
        </div>
        <span className="story-orbit orbit-one" aria-hidden="true" />
        <span className="story-orbit orbit-two" aria-hidden="true" />
      </section>

      <section className="auth-panel" aria-labelledby="auth-title">
        <div className="auth-card">
          <div className="auth-mark" aria-hidden="true">✳</div>
          <p className="eyebrow">{isRegistering ? "YOUR OWN LITTLE CORNER" : "WELCOME BACK"}</p>
          <h2 id="auth-title">{isRegistering ? "Create your account" : "Sign in to your space"}</h2>
          <p className="auth-description">
            {isRegistering
              ? "A fresh start for all the things you want to do."
              : "Your plans are right where you left them."}
          </p>

          {success && <p className="form-success" role="status">{success}</p>}

          <form className="auth-form" onSubmit={submit}>
            <label htmlFor="email">Email address</label>
            <input
              id="email"
              type="email"
              autoComplete="email"
              placeholder="you@example.com"
              maxLength={254}
              required
              value={email}
              onChange={(event) => setEmail(event.target.value)}
            />
            <label htmlFor="password">
              {isRegistering ? "6-Digit Security PIN" : "PIN or Password"}
            </label>
            <div className="password-input-wrapper">
              <input
                id="password"
                type={showPassword ? "text" : "password"}
                autoComplete={isRegistering ? "new-password" : "current-password"}
                placeholder={isRegistering ? "Enter 6 digits (e.g. 123456)" : "Enter your PIN or password"}
                inputMode={isRegistering ? "numeric" : undefined}
                pattern={isRegistering ? "[0-9]{6}" : undefined}
                title={isRegistering ? "Please enter a 6-digit numeric PIN (numbers only)" : undefined}
                minLength={isRegistering ? 6 : 1}
                maxLength={isRegistering ? 6 : 128}
                required
                value={password}
                onChange={(event) => setPassword(event.target.value)}
              />
              <button
                type="button"
                className="password-toggle-btn"
                onClick={() => setShowPassword(!showPassword)}
                aria-label={showPassword ? "Hide password" : "Show password"}
              >
                {showPassword ? "Hide" : "Show"}
              </button>
            </div>
            {isRegistering && (
              <small className="form-hint">
                Accounts use a 6-digit numeric PIN for secure and simple sign-in.
              </small>
            )}
            {error && <p className="form-error" role="alert">{error}</p>}
            <button className="primary-button auth-submit" type="submit" disabled={submitting}>
              {submitting
                ? "Please wait..."
                : isRegistering
                  ? "Create account"
                  : "Sign in"}
              {!submitting && <span aria-hidden="true">→</span>}
            </button>
          </form>

          <p className="auth-switch">
            {isRegistering ? "Already have an account?" : "New to daymark?"}{" "}
            <button
              className="text-button"
              type="button"
              onClick={() => changeMode(isRegistering ? "login" : "register")}
            >
              {isRegistering ? "Sign in" : "Create an account"}
            </button>
          </p>
          <p className="privacy-note"><span aria-hidden="true">◇</span> Your tasks are private to your account.</p>
        </div>
      </section>
    </main>
  );
}
