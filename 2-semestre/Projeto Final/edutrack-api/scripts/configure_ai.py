"""Configuração interativa local. Não imprime segredos nem faz chamadas pagas."""

import getpass
import os
import re
from pathlib import Path

from dotenv import set_key


def main():
    local = os.environ.get("LOCALAPPDATA")
    if not local:
        raise SystemExit("No servidor Linux, configure OPENAI_API_KEY e OPENAI_MODEL no gerenciador de segredos do serviço.")
    print("A chave será salva fora do Git e do OneDrive. Nenhuma chamada à IA será realizada.")
    model = input("Nome exato do modelo disponível na sua conta OpenAI: ").strip()
    if not re.fullmatch(r"[A-Za-z0-9._:-]{1,100}", model):
        raise SystemExit("Nome de modelo inválido; nenhuma configuração foi alterada.")
    key = getpass.getpass("Cole a chave de API (entrada oculta): ").strip()
    if not key.startswith("sk-") or len(key) < 30 or any(char.isspace() for char in key):
        raise SystemExit("Formato de chave inválido; nenhuma configuração foi alterada.")
    target = Path(local) / "EduTrack" / "backend.env"
    target.parent.mkdir(parents=True, exist_ok=True)
    set_key(str(target), "OPENAI_API_KEY", key)
    set_key(str(target), "OPENAI_MODEL", model)
    print("Configuração salva. Reinicie a API. Ative o consentimento na Edu IA para conversar.")
    print("Chamadas podem consumir créditos. Use limites de gasto no painel do provedor.")


if __name__ == "__main__":
    main()
