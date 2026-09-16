import hashlib
import hmac

from courtiq.resources.webhooks import verificar_assinatura


def test_verifier_accepts_prefixed_secret_and_rejects_wrong_secret():
    body = b'{"mensagem":"a\xc3\xa7\xc3\xa3o","ordem":[2,1]}'
    signature = "sha256=" + hmac.new(
        b"synthetic-secret", body, hashlib.sha256
    ).hexdigest()

    assert verificar_assinatura(body, signature, "whsec_synthetic-secret")
    assert not verificar_assinatura(body, signature, "whsec_wrong-secret")
