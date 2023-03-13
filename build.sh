#!/usr/bin/env bash
# exit on error
set -o errexit
<<<<<<< HEAD

=======
>>>>>>> 797b1a2f32889fdb0fe2fdada000e44be7d35275
poetry lock --no-update
poetry install

python manage.py collectstatic --no-input
python manage.py migrate
