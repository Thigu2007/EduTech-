import json
import os
import time
import hashlib
import re

ARQUIVO_DADOS = "usuarios.json"

def carregar_usuarios():
    if not os.path.exists(ARQUIVO_DADOS):
        return {}
    with open(ARQUIVO_DADOS, 'r', encoding='utf-8') as f:
        return json.load(f)

def salvar_usuarios(usuarios):
    with open(ARQUIVO_DADOS, 'w', encoding='utf-8') as f:
        json.dump(usuarios, f, indent=4, ensure_ascii=False)

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def validar_email(email):
    padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(padrao, email) is not None

def mostrar_menu_inicial():
    print("\n=== Bem-vindo à Plataforma EduTech+ ===")
    print("1. Cadastrar novo usuário")
    print("2. Fazer login")
    print("3. Sair")
    return input("Escolha uma opção: ")

def mostrar_menu():
    print("\n=== Menu da Plataforma ===")
    print("1. Ver cursos")
    print("2. Concluir curso")
    print("3. Ver pontuação, conquistas e missões")
    print("4. Ver ranking")
    print("5. Sair")
    return input("Escolha uma opção: ")

def mostrar_cursos():
    print("\n--- Cursos Disponíveis ---")
    print("1. Introdução ao Python")
    print("2. Segurança Digital")
    print("3. Pensamento Lógico")
    print("4. Voltar")

def concluir_curso(usuario, usuarios):
    mostrar_cursos()
    escolha = input("Digite o número do curso concluído: ")
    cursos = {
        "1": "Introdução ao Python",
        "2": "Segurança Digital",
        "3": "Pensamento Lógico"
    }
    curso = cursos.get(escolha)
    if not curso:
        print("Curso inválido.")
        return
    print(f"Parabéns! Você concluiu: {curso}")
    if curso not in usuarios[usuario]["conquistas"]:
        usuarios[usuario]["conquistas"].append(curso)
        usuarios[usuario]["pontos"] += 100
        print("🏅 Conquista desbloqueada!")
    else:
        print("Você já concluiu esse curso antes. Sem pontos extras.")
    salvar_usuarios(usuarios)

def ver_status(usuario, usuarios):
    dados = usuarios[usuario]
    print(f"\n--- Perfil de {usuario} ---")
    print(f"E-mail: {dados['email']}")
    print(f"Pontos: {dados['pontos']}")
    print("Conquistas:")
    if dados["conquistas"]:
        for c in dados["conquistas"]:
            print(f"🏅 {c}")
    else:
        print("Nenhuma conquista ainda.")
    print("Missões:")
    if dados["pontos"] >= 300:
        print("Complete todos os cursos!")
    elif dados["pontos"] >= 100:
        print("Conclua mais cursos para desbloquear mais conquistas.")
    else:
        print("Inicie sua jornada completando um curso.")

def mostrar_ranking(usuarios):
    print("\n=== Ranking dos Alunos ===")
    ranking = sorted(usuarios.items(), key=lambda item: item[1]['pontos'], reverse=True)
    for i, (nome, dados) in enumerate(ranking, 1):
        print(f"{i}º - {nome}: {dados['pontos']} pontos")

def cadastrar_usuario(usuarios):
    print("\n--- Cadastro de Novo Usuário ---")
    nome = input("Digite seu nome: ").strip()
    email = input("Digite seu e-mail: ").strip()

    if not validar_email(email):
        print("Formato de e-mail inválido. Tente novamente.")
        return None

    for dados in usuarios.values():
       if dados.get("email") == email:
            print("Este e-mail já está cadastrado. Tente outro.")
            return None

    senha = input("Crie uma senha: ").strip()
    usuarios[nome] = {
        "email": email,
        "senha": hash_senha(senha),
        "pontos": 0,
        "conquistas": []
    }
    salvar_usuarios(usuarios)
    print("Usuário cadastrado com sucesso!")
    return nome

def fazer_login(usuarios):
    print("\n--- Login ---")
    email = input("Digite seu e-mail: ").strip()

    usuario_encontrado = None
    for nome, dados in usuarios.items():
        if dados.get("email") == email:
            usuario_encontrado = nome
            break

    if not usuario_encontrado:
        print("Email incorreto. Encerrando o programa.")
        return None

    nome_digitado = input("Digite seu nome: ").strip()
    if nome_digitado != usuario_encontrado:
        print("Nome não corresponde ao email fornecido. Encerrando o programa.")
        return None

    senha = input("Digite sua senha: ").strip()
    if usuarios[nome_digitado]["senha"] == hash_senha(senha):
        print(f"Bem-vindo de volta, {nome_digitado}!")
        return nome_digitado
    else:
        print("Senha incorreta. Encerrando o programa.")
        return None

def main():
    usuarios = carregar_usuarios()
    usuario_logado = None

    while True:
        escolha = mostrar_menu_inicial()
        if escolha == "1":
            usuario_logado = cadastrar_usuario(usuarios)
        elif escolha == "2":
            usuario_logado = fazer_login(usuarios)
        elif escolha == "3":
            print("Saindo... Até logo!")
            return
        else:
            print("Opção inválida.")
            continue

        if usuario_logado:
            break
        time.sleep(1)

    while True:
        opcao = mostrar_menu()
        if opcao == "1":
            mostrar_cursos()
        elif opcao == "2":
            concluir_curso(usuario_logado, usuarios)
        elif opcao == "3":
            ver_status(usuario_logado, usuarios)
        elif opcao == "4":
            mostrar_ranking(usuarios)
        elif opcao == "5":
            print("Saindo... Até logo!")
            break
        else:
            print("Opção inválida.")
        time.sleep(1)

if __name__ == "__main__":
    main()
