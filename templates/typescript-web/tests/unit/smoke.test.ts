/**
 * Smoke test for the unit suite.
 *
 * Replace this with real unit tests. Every suite ships with at least one test
 * so a freshly scaffolded project has a green quality gate from its first
 * commit.
 */
import { afterEach, describe, expect, it, vi } from "vitest";

import { apiFetch } from "@/lib/api";

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("apiFetch", () => {
  it("returns the decoded body on success", async () => {
    vi.stubGlobal("fetch", async () => Response.json({ status: "ok" }));
    await expect(apiFetch<{ status: string }>("/api/health")).resolves.toEqual({ status: "ok" });
  });

  it("surfaces non-2xx responses as errors", async () => {
    vi.stubGlobal(
      "fetch",
      async () => new Response("nope", { status: 500, statusText: "Server Error" }),
    );
    await expect(apiFetch("/api/health")).rejects.toThrow("API error: 500");
  });
});
