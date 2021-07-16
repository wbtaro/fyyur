# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import json
from datetime import datetime
import dateutil.parser
import babel
from flask import (
    render_template,
    request,
    flash,
    redirect,
    url_for
)
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from sqlalchemy.orm import backref
from .forms import *
from .models import Venue, Artist, Genre, Show
from . import app, db

# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    value = value.strftime('%Y-%m-%d %H:%M:%S')
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime

# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#


@app.route('/')
def index():
    venues = Venue.query.order_by(db.desc(Venue.created_at)).limit(10).all()
    artists = Artist.query.order_by(db.desc(Artist.created_at)).limit(10).all()
    return render_template('pages/home.html', venues=venues, artists=artists)


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    venues = Venue.query.all()
    data = []
    for venue in venues:
        area_existed = False
        for area in data:
            if area['city'] == venue.city and area['state'] == venue.state:
                area_existed = True
                area['venues'].append(venue)

        if not area_existed:
            area = {}
            area['city'] = venue.city
            area['state'] = venue.state
            area['venues'] = [venue]
            data.append(area)

    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_term = request.form.get('search_term', '')
    venues = Venue. \
        query. \
        filter(Venue.name.ilike('%' + search_term + '%')). \
        order_by(Venue.name). \
        all()
    response = {
        "count": len(venues),
        "data": []
    }
    response['data'] = [venue for venue in venues]

    return render_template(
        'pages/search_venues.html',
        results=response,
        search_term=search_term
    )


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue = Venue.query.get(venue_id)
    print(venue.upcoming_shows)
    return render_template('pages/show_venue.html', venue=venue)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    try:
        form = VenueForm(request.form)
        if not form.validate():
            for item, error in form.errors.items():
                flash(item + ': ' + error[0])
            return render_template('forms/new_venue.html', form=form)

        venue = Venue(
            name=form.name.data,
            city=form.city.data,
            state=form.state.data,
            address=form.address.data,
            phone=form.phone.data,
            image_link=form.image_link.data,
            facebook_link=form.facebook_link.data,
            website_link=form.website_link.data,
            seeking_talent=form.seeking_talent.data,
            seeking_description=form.seeking_description.data,
            created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            updated_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )

        for genre in form.genres.data:
            venue_genre = Genre.query.filter_by(name=genre).one()
            venue.genres.append(venue_genre)

        db.session.add(venue)
        db.session.commit()

        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except Exception as e:
        db.session.rollback()
        app.logger.warning(e)
        flash(
            'An error occurred. Venue ' +
            form.name.data +
            ' could not be listed.'
        )
        return render_template('forms/new_venue.html', form=form)
    finally:
        db.session.close()

    return render_template('pages/home.html')


# @app.route('/venues/<venue_id>', methods=['DELETE'])
@app.route('/venues/<venue_id>/delete', methods=['POST'])
def delete_venue(venue_id):
    try:
        Venue.query.filter_by(id=venue_id).delete()
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully deleted!')
    except Exception as e:
        app.logger.warning(e)
        db.session.rollback
        flash(
            'An error occurred. Venue ' +
            request.form['name'] +
            ' could not be deleted.'
        )
    finally:
        db.session.close

    return redirect(url_for('index', code=303))


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    data = Artist.query.all()
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    search_term = request.form.get('search_term', '')
    artists = Artist. \
        query. \
        filter(Artist.name.ilike('%' + search_term + '%')). \
        order_by(Artist.name). \
        all()
    response = {
        "count": len(artists),
        "data": []
    }
    response['data'].append(artists)
    return render_template(
        'pages/search_artists.html',
        results=response,
        search_term=request.form.get('search_term', '')
    )


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    artist = Artist.query.get(artist_id)
    return render_template('pages/show_artist.html', artist=artist)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.get(artist_id)

    form.name.data = artist.name
    form.city.data = artist.city
    form.state.data = artist.state
    form.phone.data = artist.phone
    form.image_link.data = artist.image_link
    form.facebook_link.data = artist.facebook_link
    form.website_link.data = artist.website_link
    form.seeking_venue.data = artist.seeking_venue
    form.seeking_description.data = artist.seeking_description
    form.genres.data = [genre for genre in artist.genres]
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    try:
        form = ArtistForm(request.form)
        artist = Artist.query.get(artist_id)

        if not form.validate():
            for item, error in form.errors.items():
                flash(item + ': ' + error[0])
            return render_template(
                'forms/edit_artist.html',
                form=form,
                artist=artist
            )

        artist.genres.clear()
        db.session.add(artist)

        artist.name = form.name.data
        artist.city = form.city.data
        artist.state = form.state.data
        artist.phone = form.phone.data
        artist.image_link = form.image_link.data
        artist.facebook_link = form.facebook_link.data
        artist.website_link = form.website_link.data
        artist.seeking_venue = form.seeking_venue.data
        artist.seeking_description = form.seeking_description.data
        artist.updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        for genre in form.genres.data:
            artist_genre = Genre.query.filter_by(name=genre).one()
            artist.genres.append(artist_genre)

        db.session.add(artist)
        db.session.commit()

        flash('Artist ' + request.form['name'] + ' was successfully updated!')
    except Exception as e:
        db.session.rollback()
        app.logger.warning(e)
        flash(
            'An error occurred. Venue ' +
            artist.name +
            ' could not be updated.'
        )
        return render_template(
            'forms/edit_artist.html',
            form=form,
            artist=artist
        )
    finally:
        db.session.close()

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.get(venue_id)

    form.name.data = venue.name
    form.city.data = venue.city
    form.state.data = venue.state
    form.address.data = venue.address
    form.phone.data = venue.phone
    form.image_link.data = venue.image_link
    form.facebook_link.data = venue.facebook_link
    form.website_link.data = venue.website_link
    form.seeking_talent.data = venue.seeking_talent
    form.seeking_description.data = venue.seeking_description
    form.genres.data = [genre for genre in venue.genres]
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    try:
        form = VenueForm(request.form)
        venue = Venue.query.get(venue_id)

        if not form.validate():
            for item, error in form.errors.items():
                flash(item + ': ' + error[0])
            return render_template(
                'forms/edit_venue.html',
                form=form,
                venue=venue
            )

        venue.genres.clear()
        db.session.add(venue)

        venue.name = form.name.data
        venue.city = form.city.data
        venue.state = form.state.data
        venue.address = form.address.data
        venue.phone = form.phone.data
        venue.image_link = form.image_link.data
        venue.facebook_link = form.facebook_link.data
        venue.website_link = form.website_link.data
        venue.seeking_talent = form.seeking_talent.data
        venue.seeking_description = form.seeking_description.data
        venue.updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        for genre in form.genres.data:
            venue_genre = Genre.query.filter_by(name=genre).one()
            venue.genres.append(venue_genre)

        db.session.add(venue)
        db.session.commit()

        flash('Venue ' + request.form['name'] + ' was successfully updated!')
    except Exception as e:
        db.session.rollback()
        app.logger.warning(e)
        flash(
            'An error occurred. Venue ' +
            venue.name +
            ' could not be updated.'
        )
    finally:
        db.session.close()

    return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    try:
        form = ArtistForm(request.form)
        if not form.validate():
            for item, error in form.errors.items():
                flash(item + ': ' + error[0])
            return render_template('forms/new_artist.html', form=form)

        artist = Artist(
            name=form.name.data,
            city=form.city.data,
            state=form.state.data,
            phone=form.phone.data,
            image_link=form.image_link.data,
            facebook_link=form.facebook_link.data,
            website_link=form.website_link.data,
            seeking_venue=form.seeking_venue.data,
            seeking_description=form.seeking_description.data,
            created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            updated_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )

        for genre in form.genres.data:
            artist_genre = Genre.query.filter_by(name=genre).one()
            artist.genres.append(artist_genre)

        db.session.add(artist)
        db.session.commit()

        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except Exception as e:
        db.session.rollback()
        app.logger.warning(e)
        flash(
            'An error occurred. Venue ' +
            form.name.data +
            ' could not be listed.'
        )
    finally:
        db.session.close()

    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    shows = Show.query.all()
    return render_template('pages/shows.html', shows=shows)


@app.route('/shows/create')
def create_shows():
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    try:
        form = ShowForm(request.form)
        print(form.errors)
        if not form.validate():
            print(form.errors)
            for item, error in form.errors.items():
                flash(item + ': ' + error[0])
                return render_template('forms/new_show.html', form=form)

        show = Show(
            artist_id=form.artist_id.data,
            venue_id=form.venue_id.data,
            start_time=form.start_time.data
        )

        db.session.add(show)
        db.session.commit()

        flash('Show was successfully listed!')

    except Exception as e:
        db.session.rollback()
        app.logger.warning(e)
        flash('An error occurred. Show could not be listed.')
    finally:
        db.session.close()

    return render_template('pages/home.html')


@app.errorhandler(400)
def bad_request_error(error):
    return render_template('errors/400.html'), 400


@app.errorhandler(401)
def unauthorized_error(error):
    return render_template('errors/401.html'), 401


@app.errorhandler(403)
def access_frobidden_error(error):
    return render_template('errors/403.html'), 403


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(405)
def method_not_allowed_error(error):
    return render_template('errors/405.html'), 405


@app.errorhandler(409)
def conflict_error(error):
    return render_template('errors/409.html'), 409


@app.errorhandler(422)
def unprocessable_entity_error(error):
    return render_template('errors/422.html'), 422


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: \
            %(message)s [in %(pathname)s:%(lineno)d]'
        )
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
