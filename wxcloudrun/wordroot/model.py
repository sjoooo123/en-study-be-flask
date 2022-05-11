from datetime import datetime

from wxcloudrun import db


# 前缀表
class Wordroot(db.Model):
    # 设置结构体表格名称
    __tablename__ = 'Wordroot'

    # 设定结构体对应表格的字段
    id = db.Column(db.Integer, primary_key=True)
    wordroot = db.Column(db.String(255), nullable=False)
    translation = db.Column(db.String(2048))
    mean = db.Column(db.String(2048))
    example = db.Column(db.String(2048))
    category = db.Column(db.Integer)
    note = db.Column(db.String(2048))
    created_at = db.Column('createdAt', db.TIMESTAMP,
                           nullable=False, default=datetime.now())
    updated_at = db.Column('updatedAt', db.TIMESTAMP,
                           nullable=False, default=datetime.now())
