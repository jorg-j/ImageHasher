
# Image Hasher

An image hashing written in Python. 

Supports:

* Average hashing
* Perceptual hashing
* Difference hashing
* Wavelet hashing
* HSV color hashing (colorhash)
* Crop-resistant hashing

## Rationale

Image hashes tell whether two images look nearly identical.
This is different from cryptographic hashing algorithms (like MD5, SHA-1)
where tiny changes in the image give completely different hashes. 
In image fingerprinting, we actually want our similar inputs to have
similar output hashes as well.

The image hash algorithms (average, perceptual, difference, wavelet)
analyse the image structure on luminance (without color information).
The color hash algorithm analyses the color distribution and 
black & gray fractions (without position information).

## Storage


In order to find images which are nearly identical the hashes for each
file are stored in a sqlite3 database.
This enables a quick command to locate duplicate images within the db without
performing a one-to-many search.

## Searching


To easily search the database for duplicate hashes

`
SELECT filename, ahash FROM hashes
WHERE ahash in (
SELECT ahash FROM hashes GROUP BY ahash HAVING COUNT(id)>1)
ORDER BY ahash;
`

This query will generate a table of filenames

| filename | ahash |
|----------|-------|
| foo      | aaa   |
| baa      | aaa   |
| foo1     | abb   |
| baa3     | abb   |


## Usage

- Populate the directory of choice with images
- Set the directory in the config under source
- Ensure the config heading is set in the imhash.py file
- Set the pool size. (There is a semaphore print out to assist in tuning the pool size)
- Run imhash.py

## Docker

When configuring for docker do not adjust the config.ini or imhash.py config settings.

During build the `SA` config in imhash.py will automatically be converted to `Docker`.
With the config.ini data mapping to the paths inside the docker image.

The host directory volumes can be set in the docker-compose.yaml

`
    volumes:
      - ~/Documents/docker/imghash/data:/code/data
      - ~/Documents/docker/imghash/new:/code/new
      - ~/Documents/docker/imghash/source:/code/source
`

To build:

`docker build -t imghash .`

To run:

`docker-compose up`

To inspect:

`docker run -it --entrypoint /bin/bash imghash`