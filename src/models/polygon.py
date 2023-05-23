from src.utils.ext import db
# from src.models.user import User

class Polygon(db.Model):
    __tablname__ = 'polygon'

    id = db.Column(db.Integer, primary_key = True)
    cad_number = db.Column(db.String(255), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"))

    def save(self):
        db.session.add(self)
        db.session.commit()
        
    # def format_2(self)""
    # style = db.relationship("Style", backref="style", uselist=False)

# class Style(db.Model):
#     __tablname__ = 'style'

#     id = db.Column(db.Integer, primary_key = True)
#     color = db.Column(db.String(100))
#     weight = db.Column(db.Float())
#     opacity = db.Column(db.Float())
#     fillColor = db.Column(db.String(100))
#     fillOpacity = db.Column(db.Float())
#     dashArray_line = db.Column(db.Float())
#     dashArray_space = db.Column(db.Float())
#     polygon_cad_number = db.Column(db.String(255), db.ForeignKey('polygon.cad_number', ondelete="CASCADE"), unique=True)