from app import criar_app

app = criar_app()

# se este ficheiro está a ser chamado por nós
# e não como importação de algo por um outro
# ... corre a app
if __name__ == "__main__":
    app.run(debug=True)