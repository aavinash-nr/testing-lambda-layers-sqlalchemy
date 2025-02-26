import json
import csv
from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class BirthRecord(Base):
    __tablename__ = 'births'
    id = Column(Integer, Sequence('birth_id_seq'), primary_key=True)
    year = Column(Integer)
    state = Column(String(50))
    sex = Column(String(1))
    births = Column(Integer)

def lambda_handler(event, context):
    db_path = '/tmp/births.db'

    engine = create_engine(f'sqlite:///{db_path}')

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    csv_file_path = '/var/task/births.csv' 

    with open(csv_file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            new_record = BirthRecord(
                year=int(row['year']),
                state=row['state'],
                sex=row['sex'],
                births=int(row['births'])
            )
            session.add(new_record)
    
    session.commit()

    all_records = session.query(BirthRecord).all()
    records_list = [
        {'id': record.id, 'year': record.year, 'state': record.state, 'sex': record.sex, 'births': record.births}
        for record in all_records
    ]

    session.close()

    return {
        'statusCode': 200,
        'body': json.dumps(len(records_list))
    }
