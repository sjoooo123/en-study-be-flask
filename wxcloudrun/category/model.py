from datetime import datetime

from wxcloudrun import db


# 分类表
class Category(db.Model):
    # 设置结构体表格名称
    __tablename__ = 'Category'

    # 设定结构体对应表格的字段
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column('createdAt', db.TIMESTAMP,
                           nullable=False, default=datetime.now())
    updated_at = db.Column('updatedAt', db.TIMESTAMP,
                           nullable=False, default=datetime.now())
