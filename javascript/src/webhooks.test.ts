import { describe, expect, it } from "vitest";

import { verificarAssinatura } from "./webhooks";

describe("verificarAssinatura", () => {
  it("verifies a signature produced by the Python SDK's HMAC implementation", async () => {
    await expect(
      verificarAssinatura({
        payload: '{"mensagem":"ação","ordem":[2,1]}',
        signature:
          "sha256=0448e6c483434a6d2c81d05d610df329d07b89b8a6affb86814c15040f14593c",
        secret: "whsec_synthetic-secret",
      }),
    ).resolves.toBe(true);
  });
});
