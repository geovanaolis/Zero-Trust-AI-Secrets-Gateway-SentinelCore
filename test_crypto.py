from src.domain.crypto import EnvelopeCryptoManager

# Simula uma Master Key do ambiente
MASTER_KEY = "minha_senha_mestre_super_segura_123"
OPENAI_KEY_REPOSITORIO = "sk-proj-abc123456789xyzsecretllmkey"

crypto = EnvelopeCryptoManager(master_secret=MASTER_KEY)

# Criptografando antes de enviar ao Banco de Dados
texto_cifrado = crypto.encrypt(OPENAI_KEY_REPOSITORIO)
print("--- CHAVE CRIPTOGRAFADA (O QUE VAI PARA O POSTGRES) ---")
print(texto_cifrado)

# Descriptografando na hora de usar
texto_original = crypto.decrypt(texto_cifrado)
print("\n--- CHAVE DESCRIPTOGRAFADA (USO INTERNO) ---")
print(texto_original)

assert texto_original == OPENAI_KEY_REPOSITORIO, "Erro: A descriptografia falhou!"
print("\n✅ Teste de criptografia concluído com sucesso!")