from datetime import datetime
import re
from flask_wtf import Form
from werkzeug.utils import ArgumentValidationError
from wtforms import (
    StringField,
    SelectField,
    SelectMultipleField,
    DateTimeField,
    BooleanField,
    FieldList
)
from wtforms.fields.core import FormField
from wtforms.validators import (
    DataRequired,
    URL,
    Regexp,
    Optional,
    ValidationError
)
from .models import Artist, Genre, Venue


def validate_genres(form, field):
    genres = field.data
    expected_genres = [genre.name for genre in Genre.query.all()]
    for genre in genres:
        if genre not in expected_genres:
            raise ValidationError('genres: invalid genre')

def validate_available_start_and_end_time(form, field):
    if not (form.start_time.data or form.end_time.data):
        pass
    elif not (form.start_time.data and form.end_time.data):
        raise ValidationError('Input both Start Time and End Time')
    elif form.start_time.data >= form.end_time.data:
        raise ValidationError('End Time must be later than Start Time')


def validate_start_and_end_time(form, field):
    if form.start_time.data >= form.end_time.data:
        raise ValidationError('End Time must be later than Start Time')


def artist_is_available(form, field):
    artist = Artist.query.get(form.artist_id.data)
    start_time = form.start_time.data
    end_time = form.end_time.data
    available = False
    for available_time in artist.available_datetimes:
        if (
            available_time.start_time <= start_time and
            available_time.end_time >= end_time
        ):
            available = True

    if not available:
        raise ValidationError(
            'this artist is not available in this time'
        )


class ShowForm(Form):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[
            DataRequired(),
            validate_start_and_end_time,
            artist_is_available
        ],
        default=datetime.today(),
        format='%Y-%m-%d %H:%M'
    )
    end_time = DateTimeField(
        'end_time',
        validators=[DataRequired(), validate_start_and_end_time],
        default=datetime.today(),
        format='%Y-%m-%d %H:%M'
    )

    def validate_artist_id(form, field):
        artist_ids = [artist.id for artist in Artist.query.all()]
        if int(field.data) not in artist_ids:
            raise ValidationError(
                'artist id ' +
                field.data +
                ' does not exist'
            )

    def validate_venue_id(form, field):
        venue_ids = [venue.id for venue in Venue.query.all()]
        if int(field.data) not in venue_ids:
            raise ValidationError(
                'venue id ' +
                field.data +
                ' does not exist'
            )


class VenueForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone',
        validators=[
            Optional(),
            Regexp(
                '^[0-9]{3}[-][0-9]{3}[-][0-9]{4}$',
                message='phone number must be in format xxx-xxx-xxxx'
            )
        ]
    )
    image_link = StringField(
        'image_link',
        default='',
        validators=[Optional(), URL()]
    )
    genres = SelectMultipleField(
        'genres',
        validators=[
            DataRequired(),
            validate_genres
        ],
        choices=[(genre.name, genre.name) for genre in Genre.query.all()]
    )
    facebook_link = StringField(
        'facebook_link',
        validators=[Optional(), URL()]
    )
    website_link = StringField(
        'website_link',
        validators=[Optional(), URL()]
    )

    seeking_talent = BooleanField('seeking_talent')

    seeking_description = StringField(
        'seeking_description'
    )

class AvailableTimeForm(Form):
    class Meta:
        csrf = False

    start_time = DateTimeField(
        'start_time',
        validators=[Optional(), validate_available_start_and_end_time],
        format='%Y-%m-%d %H:%M'
    )

    end_time = DateTimeField(
        'end_time',
        validators=[Optional(), validate_available_start_and_end_time],
        format='%Y-%m-%d %H:%M'
    )

class ArtistForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )

    phone = StringField(
        'phone',
        validators=[
            Optional(),
            Regexp(
                '^[0-9]{3}[-][0-9]{3}[-][0-9]{4}$',
                message='phone number must be in format xxx-xxx-xxxx'
            )
        ]
    )

    image_link = StringField(
        'image_link',
        default='',
        validators=[Optional(), URL()]
    )
    genres = SelectMultipleField(
        'genres',
        validators=[
            DataRequired(),
            validate_genres
        ],
        choices=[(genre.name, genre.name) for genre in Genre.query.all()]
    )

    facebook_link = StringField(
        'facebook_link',
        validators=[Optional(), URL()]
    )

    website_link = StringField(
        'website_link',
        validators=[Optional(), URL()]
    )

    seeking_venue = BooleanField('seeking_venue')

    seeking_description = StringField(
        'seeking_description'
    )

    available_times = FieldList(
        FormField(AvailableTimeForm),
        min_entries=3,
        max_entries=3
        )
