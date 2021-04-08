def test_as_configuracoes_do_app_devem_ser_adequadas_para_testes(app):
    assert app.config["DEBUG"] == False
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///:memory:"
    assert app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] == False
    assert app.config["UPLOAD_FOLDER_IMG"] == "media/img"
    assert app.config["UPLOAD_FOLDER_DOC"] == "media/doc"
    assert app.config["SECRET_KEY"] == "test"
