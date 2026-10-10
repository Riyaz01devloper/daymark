export class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

export async function apiRequest(url, options = {}) {
  const response = await fetch(url, {
    credentials: "include",
    ...options,
    headers: {
      ...(options.body ? { "Content-Type": "application/json" } : {}),
      ...options.headers,
    },
  });

  if (!response.ok) {
    let message = `Request failed (${response.status})`;
    try {
      const body = await response.json();
      if (body.detail) {
        const cleanMsg = (msg) => (typeof msg === "string" ? msg.replace(/^Value error,\s*/i, "") : msg);
        message = Array.isArray(body.detail)
          ? body.detail.map((item) => cleanMsg(item.msg)).filter(Boolean).join(". ")
          : cleanMsg(body.detail);
      }
    } catch {
      // Keep the HTTP status message when the response has no JSON body.
    }
    throw new ApiError(message, response.status);
  }

  return response.status === 204 ? null : response.json();
}
