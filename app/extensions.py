def get_db():
    from app import engine
    from sqlalchemy.orm import sessionmaker

    Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = Sessionlocal()
    try:
        yield db

    finally:
        db.close()