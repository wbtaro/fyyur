from datetime import datetime

from . import db

venue_genres = db.Table(
    'venue_genres',
    db.Column(
        'venue_id',
        db.Integer,
        db.ForeignKey('venues.id', ondelete="cascade"),
        primary_key=True
    ),
    db.Column(
        'genre',
        db.String,
        db.ForeignKey('genres.name', ondelete="cascade"),
        primary_key=True
    )
)

artist_genres = db.Table(
    'artist_genres',
    db.Column(
        'artist_id',
        db.Integer,
        db.ForeignKey('artists.id', ondelete="cascade"),
        primary_key=True
    ),
    db.Column(
        'genre',
        db.String,
        db.ForeignKey('genres.name', ondelete="cascade"),
        primary_key=True
    )
)


class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    genres = db.relationship(
        'Genre',
        secondary=venue_genres,
        backref=db.backref('venues', lazy=True),
        cascade="all, delete"
    )
    shows = db.relationship(
        'Show',
        backref='venue',
        lazy=True,
        cascade='all, delete, delete-orphan'
    )

    @property
    def upcoming_shows(self):
        return [
            show for show in self.shows
            if show.start_time >= datetime.now()
        ]

    @property
    def num_upcoming_shows(self):
        return len(self.upcoming_shows)

    @property
    def past_shows(self):
        return [
            show for show in self.shows
            if show.start_time < datetime.now()
        ]

    @property
    def num_past_shows(self):
        return len(self.past_shows)


class Genre(db.Model):
    __tablename__ = 'genres'
    name = db.Column(db.String, primary_key=True)


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    genres = db.relationship(
        'Genre',
        secondary=artist_genres,
        backref=db.backref('artists', lazy=True),
        cascade="all, delete"
    )
    shows = db.relationship(
        'Show',
        backref='artist',
        lazy=True,
        cascade='all, delete, delete-orphan'
    )

    @property
    def upcoming_shows(self):
        return [
            show for show in self.shows
            if show.start_time >= datetime.now()
        ]

    @property
    def num_upcoming_shows(self):
        return len(self.upcoming_shows)

    @property
    def past_shows(self):
        return [
            show for show in self.shows
            if show.start_time < datetime.now()
        ]

    @property
    def num_past_shows(self):
        return len(self.past_shows)


class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(
        db.Integer,
        db.ForeignKey('artists.id', ondelete='cascade'),
        nullable=False
    )
    venue_id = db.Column(
        db.Integer,
        db.ForeignKey('venues.id', ondelete='cascade'),
        nullable=False
    )
    start_time = db.Column(
        db.DateTime,
        nullable=False
    )
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
