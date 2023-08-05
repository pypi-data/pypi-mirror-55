" Extract frames from or assemble frames into a video "

# Standard imports
import os
import argparse
import json
import struct
import logging
from itertools import count
from fnmatch import fnmatch

# Library imports
import cv2
from tqdm import trange, tqdm


def mkdir_like(hint="frames"):
    " Create and return directory with name similar (or identical) to 'hint' "
    dirname = hint
    suffix = 1
    while os.path.exists(dirname):
        dirname = "{}_{:d}".format(hint, suffix)
        suffix += 1
    os.makedirs(dirname)
    return dirname


def default_videofilename(hint="video", extension=".mp4"):
    " Find an available filename similar (or identical) to 'hint' "
    for i in count():
        suffix = ('_' + str(i)) if i else ''
        videofilename = ''.join((hint, suffix, extension))
        if not os.path.exists(videofilename):
            return videofilename


def extract(videofilename, outdir=None):
    " Extract the frames from 'videofilename' and store them in 'outdir' "
    assert os.path.isfile(videofilename)

    hint = os.path.basename(videofilename).rsplit('.', 1)[0]
    if outdir is None:
        outdir = mkdir_like(hint)
    else:
        if os.path.exists(outdir):
            return "Output directory {!r} already exists. Aborting.".format(outdir)
        os.makedirs(outdir)

    # Open video file and extract info about the file, save it in json
    vidcap = cv2.VideoCapture(videofilename)
    frame_count = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    encoded_fourcc = vidcap.get(cv2.CAP_PROP_FOURCC)
    fourcc = struct.pack('i', int(encoded_fourcc)).decode()
    info = {
        #"width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        #"height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        "fps": vidcap.get(cv2.CAP_PROP_FPS),
        "fourcc": fourcc
    }
    with open(os.path.join(outdir, 'info.json'), 'w') as f:
        json.dump(info, f)

    # Print a status update
    headline = "Extracting {} frames of {!r} to directory {!r}"
    logging.info(headline.format(frame_count, videofilename, outdir))

    # Read frames from the video and write them to image files
    filename_template = "frame{{:0{}d}}.jpg".format(len(str(frame_count)))
    for i in trange(frame_count, unit="frames"):
        success, image = vidcap.read()
        assert success, "Error reading frame {}".format(i)
        filename = os.path.join(outdir, filename_template.format(i))
        cv2.imwrite(filename, image)

    return 0


def _get_fps_fourcc(directory, videofilename, default_fps=25.0):
    " Get framerate and 4cc code from info.json else use defaults "
    json_filename = os.path.join(directory, "info.json")
    if os.path.isfile(json_filename):
        with open(json_filename) as f:
            info = json.load(f)
        fps = info["fps"]
        fourcc = info["fourcc"]
    else:
        # use defaults
        fps = default_fps
        assert videofilename.lower().endswith(".mp4"), \
               "Target filename must be a .mp4 file (not {!r})".format(\
               videofilename)
    return fps, fourcc


def assemble(directory, videofilename=None):
    " Assemble image frames from given directory into a video file "
    assert os.path.isdir(directory),\
           "{!r} is not a directory".format(directory)

    directory = directory.rstrip('/')

    if videofilename is None:
        videofilename = default_videofilename(directory)

    # Get framerate and 4cc code from info.json else use defaults "
    fps, fourcc = _get_fps_fourcc(directory, videofilename)

    # Sort image filenames from source directory by filename
    pattern = "frame*.jpg"
    image_filenames = sorted([os.path.join(directory, fn)
                              for fn in os.listdir(directory)
                              if fnmatch(fn, pattern)])

    assert image_filenames,\
           "No files match pattern {!r} in {!r}".format(pattern, directory)

    # Get image properties of first frame to enable verification that all
    # subsequent frames have the same dimanesions and number of channels
    height, width, channels = cv2.imread(image_filenames[0]).shape


    prefix, extension = videofilename.rsplit('.', 1)
    combos = [(fourcc, extension), ("mp4v", "mp4"), ("H264", "mkv"), ("MJPG", "avi")]

    for fourcc, extension in combos:
        videofilename = prefix + '.' + extension
        encoded_fourcc = cv2.VideoWriter_fourcc(*fourcc)
        video = cv2.VideoWriter(videofilename, encoded_fourcc, fps, (width, height))

        # Check for success of opening the video file
        if video.isOpened():
            break

        logging.warning("Could not open video writer for %r with fourcc %r",
                        videofilename, fourcc)

    else:
        # The following prints out available FOURCC codes
        video = cv2.VideoWriter(videofilename, -1, fps, (width, height))
        logging.error("Failed to write video file. No available codecs. "
                      "Recompile OpenCV with FFMPEG library linking.")

        return 1

    # Assemble the video
    logging.info("Assembling {} frames from {!r} into {!r} ({}, {} fps)".format(\
                 len(image_filenames), directory, videofilename, fourcc, fps))
    for image_filename in tqdm(image_filenames, unit="frames"):
        image = cv2.imread(image_filename)
        assert image.shape == (height, width, channels), \
               "{!r} has mismatched shape {} (expected {})".format(\
               image_filename, image.shape, (height, width, channels))
        video.write(image)
    video.release()

    return 0


def auto(source, target):
    " Either assemble or disassemble a video from/to frame images "

    # If source is a directory, assemble its image files into a video
    if os.path.isdir(source):
        return assemble(source, target)

    # Else if source is a (video) file, extract its frames to a directory
    if os.path.isfile(source):
        return extract(source, target)

    return "No such file or directory {!r}".format(source)


def main():
    " Main command-line entrypoint "
    logging.basicConfig(level=logging.DEBUG, format="%(message)s")
    desc = "Extract frames from or assemble frames into a video"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("source", metavar="source")
    parser.add_argument("-o", dest="target", nargs='?', default=None)
    kwargs = vars(parser.parse_args())
    return auto(**kwargs)


if __name__ == "__main__":
    import sys
    sys.exit(main())
