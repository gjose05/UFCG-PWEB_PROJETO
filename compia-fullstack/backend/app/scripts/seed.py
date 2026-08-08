from decimal import Decimal
from sqlalchemy import select
from app.db import SessionLocal
from app.config import settings
from app.models import User,Product
from app.security import hash_password
P=[
('fundamentos-inteligencia-artificial','Fundamentos de Inteligência Artificial','Equipe COMPIA','Inteligência Artificial','physical','89.90','109.90',18,'book-a','Uma introdução prática aos conceitos essenciais de IA.'),
('arquitetura-software-inteligente','Arquitetura de Software Inteligente','Marina Costa','Arquitetura','physical','99.90',None,12,'book-b','Padrões e decisões arquiteturais para sistemas inteligentes.'),
('blockchain-criptografia-aplicada','Blockchain e Criptografia Aplicada','Rafael Lima','Blockchain','digital','54.90',None,999,'book-c','Conceitos de blockchain, hashes e criptografia aplicada.'),
('ciberseguranca-sistemas-modernos','Cibersegurança para Sistemas Modernos','Ana Ribeiro','Cibersegurança','physical','79.90',None,20,'book-a','Boas práticas para proteger aplicações e dados.'),
('machine-learning-pratica','Machine Learning na Prática','Carlos Almeida','Inteligência Artificial','digital','62.90',None,999,'book-b','Do preparo de dados à avaliação de modelos.'),
('kit-compia-ia-seguranca','Kit COMPIA: IA + Segurança','Vários autores','Kits','kit','159.90','189.80',7,'book-c','Kit promocional com dois títulos selecionados.')]
def run():
    db=SessionLocal()
    if not db.scalar(select(User).where(User.email==settings.admin_email.lower())): db.add(User(full_name='Administrador COMPIA',email=settings.admin_email.lower(),password_hash=hash_password(settings.admin_password),role='admin'))
    if not db.scalar(select(Product.id).limit(1)):
        for slug,title,author,cat,typ,price,old,stock,color,desc in P: db.add(Product(slug=slug,title=title,author=author,category=cat,product_type=typ,price=Decimal(price),old_price=Decimal(old) if old else None,stock=stock,cover_color=color,description=desc,digital_file_url='https://example.com/ebook-demo.pdf' if typ=='digital' else None))
    db.commit(); db.close(); print('Seed concluído.')
if __name__=='__main__': run()
