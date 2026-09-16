export async function verificarAssinatura(params: {
  payload: string | ArrayBuffer;
  signature: string;
  secret: string;
}): Promise<boolean> {
  const { payload, signature, secret } = params;
  const rawSecret = secret.startsWith("whsec_") ? secret.slice("whsec_".length) : secret;

  const encoder = new TextEncoder();
  const key = await crypto.subtle.importKey(
    "raw",
    encoder.encode(rawSecret),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"],
  );

  const data =
    typeof payload === "string"
      ? encoder.encode(payload)
      : new Uint8Array(payload);

  const sig = await crypto.subtle.sign("HMAC", key, data);
  const hex = Array.from(new Uint8Array(sig))
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");

  const expected = `sha256=${hex}`;
  if (expected.length !== signature.length) return false;
  let mismatch = 0;
  for (let index = 0; index < expected.length; index += 1) {
    mismatch |= expected.charCodeAt(index) ^ signature.charCodeAt(index);
  }
  return mismatch === 0;
}
