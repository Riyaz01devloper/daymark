export class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

const API_BASE_URL = (import.meta.env.VITE_API_URL || "").replace(/\/+$/, "");
const TOKEN_STORAGE_KEY = "daymark_auth_token";

export function getAuthToken() {
  try {
    return localStorage.getItem(TOKEN_STORAGE_KEY) || "";
  } catch {
    return "";
  }
}

export function setAuthToken(token) {
  try {
    if (token) {
      localStorage.setItem(TOKEN_STORAGE_KEY, token);
    } else {
      localStorage.removeItem(TOKEN_STORAGE_KEY);
    }
  } catch {
    // Ignore storage errors in restricted contexts
  }
}

export function clearAuthToken() {
  try {
    localStorage.removeItem(TOKEN_STORAGE_KEY);
  } catch {
    // Ignore
  }
}

export async function apiRequest(url, options = {}) {
  const targetUrl = url.startsWith("http") ? url : `${API_BASE_URL}${url}`;
  const token = getAuthToken();
  const authHeaders = token ? { Authorization: `Bearer ${token}` } : {};

  const response = await fetch(targetUrl, {
    credentials: "include",
    ...options,
    headers: {
      ...authHeaders,
      ...(options.body ? { "Content-Type": "application/json" } : {}),
      ...options.headers,
    },
  });

  // Capture token from response header if provided
  const headerToken = response.headers.get("x-session-token");
  if (headerToken) {
    setAuthToken(headerToken);
  }

  if (!response.ok) {
    let message = `Request failed (${response.status})`;
    try {
      const body = await response.json();
      if (body.detail) {
        const cleanMsg = (msg) =>
          typeof msg === "string" ? msg.replace(/^Value error,\s*/i, "") : msg;
        message = Array.isArray(body.detail)
          ? body.detail.map((item) => cleanMsg(item.msg)).filter(Boolean).join(". ")
          : cleanMsg(body.detail);
      }
    } catch {
      // Keep HTTP status message when response has no JSON body
    }

    if (response.status === 401) {
      // Session expired or invalid
      clearAuthToken();
    }

    throw new ApiError(message, response.status);
  }

  if (response.status === 204) {
    return null;
  }

  const data = await response.json();
  if (data && typeof data === "object" && data.token) {
    setAuthToken(data.token);
  }
  return data;
}
