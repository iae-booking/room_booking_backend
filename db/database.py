from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://vtjwyrwhssoqzv:{password}@ec2-54-173-237-110.compute-1.amazonaws.com:5432/dab6cusmavf2j8"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'options': '-csearch_path={}'.format('booking')}  # set default schema as booking
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
