# This Dockerfile is based on: https://docs.docker.com/examples/postgresql_service/

FROM ubuntu:16.04

MAINTAINER fredrik@averpil.com

# Add the PostgreSQL PGP key to verify their Debian packages.
# It should be the same key as https://www.postgresql.org/media/keys/ACCC4CF8.asc
RUN apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8

# Add PostgreSQL's repository. It contains the most recent stable release
#     of PostgreSQL, ``9.3``.
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main" > /etc/apt/sources.list.d/pgdg.list

# Install everything in one enormous RUN command
#  There are some warnings (in red) that show up during the build. You can hide
#  them by prefixing each apt-get statement with DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \

    apt-get install -y \
    python-software-properties python-pip \
    software-properties-common \
    postgresql-9.3 postgresql-client-9.3 postgresql-contrib-9.3 postgresql-server-dev-9.3 \
    rubygems && \

    gem install taskjuggler && \

    pip install -U pip && \
    pip install sqlalchemy psycopg2 jinja2 alembic mako markupsafe python-editor nose coverage

# Note: The official Debian and Ubuntu images automatically ``apt-get clean``
# after each ``apt-get``

# Run commands as the ``postgres`` user created by the ``postgres-9.3`` package when it was ``apt-get installed``
USER postgres

RUN /etc/init.d/postgresql start && \
    psql -c "CREATE DATABASE stalker_test;" -U postgres && \
    psql -c "CREATE USER stalker_admin WITH PASSWORD 'stalker';" -U postgres && \
    /etc/init.d/postgresql stop

# Adjust PostgreSQL configuration so that remote connections to the
# database are possible.
# RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/9.3/main/pg_hba.conf

# And add ``listen_addresses`` to ``/etc/postgresql/9.3/main/postgresql.conf``
# RUN echo "listen_addresses='*'" >> /etc/postgresql/9.3/main/postgresql.conf

# Expose the PostgreSQL port
# EXPOSE 5432

# Add VOLUMEs to allow backup of config, logs and databases
# VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]

USER root

# Create symlink to TaskJuggler
# RUN ln -s $(which tj3) /usr/local/bin/tj3

# Set working directory
WORKDIR /workspace

# Embed wait-for-postgres.sh script into Dockerfile
RUN echo '\n\
# wait-for-postgres\n\
\n\

set -e\n\
\n\
cmd="$@"\n\
timer="5"\n\
\n\
until runuser -l postgres -c 'pg_isready' 2>/dev/null; do\n\
    >&2 echo "Postgres is unavailable - sleeping for $timer seconds"\n\
    sleep $timer\n\
done\n\
\n\
>&2 echo "Postgres is up - executing command"\n\
exec $cmd\n'\
>> /workspace/wait-for-postgres.sh

# Make script executable
RUN chmod +x /workspace/wait-for-postgres.sh

# Execute this when running container
ENTRYPOINT \

            # Copy stalker into container's /workspace'
            cp -r /stalker /workspace && \

            # Remove execution permissions within Stalker
            chmod -R -x /workspace/stalker && \

            # Start PostgreSQL
            runuser -l postgres -c '/usr/lib/postgresql/9.3/bin/postgres -D /var/lib/postgresql/9.3/main -c config_file=/etc/postgresql/9.3/main/postgresql.conf & ' && \

            # Wait for PostgresSQL
            ./wait-for-postgres.sh nosetests /workspace/stalker --verbosity=1 --cover-erase --with-coverage --cover-package=stalker && \

            # Cleanly shut down PostgreSQL
            /etc/init.d/postgresql stop
