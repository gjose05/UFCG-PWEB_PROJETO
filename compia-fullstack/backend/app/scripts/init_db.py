from app.db import Base,engine
import app.models
if __name__=='__main__': Base.metadata.create_all(engine); print('Banco inicializado.')
