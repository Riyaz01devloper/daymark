import { useState } from "react";
import { apiRequest } from "../api/client.js";

const grades = Array.from({ length: 12 }, (_, index) => index + 1);

export default function GradeSetup({ user, onSaved, onSignOut }) {
  const [grade, setGrade] = useState("");
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);

  async function submit(event) {
    event.preventDefault();
    setError("");
    setSaving(true);
    try {
      const updatedUser = await apiRequest("/auth/profile", {
        method: "PATCH",
        body: JSON.stringify({ grade: Number(grade) }),
      });
      onSaved(updatedUser);
    } catch (requestError) {
      setError(`Could not save your class: ${requestError.message}`);
    } finally {
      setSaving(false);
    }
  }

  return (
    <main className="grade-setup-page">
      <a className="brand" href="/" aria-label="daymark home">
        <span className="brand-icon" aria-hidden="true">d</span>
        <span>daymark</span>
      </a>
      <section className="grade-setup-card" aria-labelledby="grade-setup-title">
        <div className="auth-mark" aria-hidden="true">✳</div>
        <p className="eyebrow">A LITTLE ABOUT YOU</p>
        <h1 id="grade-setup-title">What class are you in?</h1>
        <p className="auth-description">
          We’ll use your class to make study tips more useful. You can change it later.
        </p>
        <form className="grade-setup-form" onSubmit={submit}>
          <label htmlFor="school-grade">School class</label>
          <select
            id="school-grade"
            required
            value={grade}
            onChange={(event) => setGrade(event.target.value)}
          >
            <option value="" disabled>Select your class</option>
            {grades.map((value) => (
              <option key={value} value={value}>Class {value}</option>
            ))}
          </select>
          {error && <p className="form-error" role="alert">{error}</p>}
          <button className="primary-button auth-submit" type="submit" disabled={saving || !grade}>
            {saving ? "Saving..." : "Continue"}
            {!saving && <span aria-hidden="true">→</span>}
          </button>
        </form>
        <div className="grade-setup-footer" style={{ marginTop: "20px", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <p className="grade-setup-account" style={{ margin: 0 }}>{user.email}</p>
          {onSignOut && (
            <button
              type="button"
              className="text-button"
              onClick={onSignOut}
              style={{ fontSize: "0.8rem", color: "#6e7c72", cursor: "pointer" }}
            >
              Sign out
            </button>
          )}
        </div>
      </section>
    </main>
  );
}
