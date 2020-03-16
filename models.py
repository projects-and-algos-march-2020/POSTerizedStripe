from app import db
from sqlalchemy.sql import func

likes_table = db.Table('likes', 
    db.Column('user_id', db.Integer, db.ForeignKey('users.id', ondelete="cascade"), primary_key=True), 
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id', ondelete="cascade"), primary_key=True))

# some_user.posts => [Post, Post]
class User(db.Model):	
    __tablename__ = "users"    # optional		
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45))
    last_name = db.Column(db.String(45))
    pic = db.Column(db.String(45))
    email = db.Column(db.String(45), unique=True)
    password = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=func.now())    # notice the extra import statement above
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    #NEW!
    likes_sent = db.relationship("Post", secondary=likes_table)
    #posts

    def __repr__(self):
        return f"<User: {self.email}>"

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="cascade"), nullable=False)
    author = db.relationship('User', foreign_keys=[author_id], backref="posts")

    created_at = db.Column(db.DateTime, server_default=func.now())    # notice the extra import statement above
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    #NEW! [User1, User2, User3]
    likes_rec = db.relationship("User", secondary=likes_table)

    @property
    def num_likes(self):
        # likes_rec [User1, User2]
        return len(self.likes_rec)

    def __repr__(self):
        return f"<Post: \"{self.content[:5]}...\">"

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    def string_price(self):
        return f"${round(self.price,2)}"

class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="cascade"), nullable=False)
    orderer = db.relationship('User', foreign_keys=[user_id], backref="orders")
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    order_items = db.relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete, delete-orphan"
    )
    def total_price(self):
        total = 0
        for item in self.order_items:
            total += (item.qty * item.product.price)
        return round(total,2)

class OrderItem(db.Model):
    __tablename__ = "order_items"
    id = db.Column(db.Integer, primary_key=True)
    qty = db.Column(db.Integer)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete="cascade"), nullable=False)
    product = db.relationship('Product', foreign_keys=[product_id], backref="ordered")
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    order = db.relationship('Order', foreign_keys=[order_id])
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
