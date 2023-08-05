#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: pointing
    :platform: Unix
    :synopsis: the top-level submodule of ImLine that contains the methods and classes related to ImLine's ability that is marking key points and works for creating an angular map from them.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

import cv2
import os  # Miscellaneous operating system interfaces

from imutils import paths
from tinydb import Query  # TinyDB is a lightweight document oriented database
from math import sqrt

from imline.db_fetching import DBFetcher
from imline import dot_imline_dir
from imline import log_manager

logger = log_manager.get_logger(__name__, "DEBUG")


class Mapper:
    """Class to define an ability that is for mapping with lines that creates from key-points.

    This class provides necessary initiations and functions named :func:`t_system.recordation.RecordManager.start`
    for creating a Record object and start recording by this object.
    """

    def __init__(self, out_path):
        """Initialization method of :class:`t_system.mapping.Mapper` class.

        Args:
                out_path:       	    Path that kepps processed images and key-point coordinates.
        """

        self.out_folder = out_path if out_path else f'{dot_imline_dir}/out_{len(next(os.walk(dot_imline_dir))[1])}'
        self.mapped_img_folder = f'{self.out_folder}/mapped_images'

        self.__check_folders()

        self.db = DBFetcher(self.out_folder, "db").fetch()

        self.current_img = None
        self.current_img_backup = None
        self.current_img_name = None

        self.key_points = []
        self.current_key_point = ()

    def start_by(self, raw_dataset=None, ripe_dataset=None):
        """Method to start mapping of given dataset. If raw dataset given, first start the specifying key-points.

        Args:
            raw_dataset:                Image dataset folder that contains only unprocessed images.
            ripe_dataset:               Dataset folder that contains images and key-points data.
        """

        if raw_dataset:

            image_paths = list(paths.list_images(raw_dataset))

            for (i, imagePath) in enumerate(image_paths):
                # extract the person name from the image path
                print("[INFO] processing image {}/{}".format(i + 1,
                                                             len(image_paths)))
                self.current_img_name = imagePath.split(os.path.sep)[-1]

                self.current_img = cv2.imread(imagePath)
                # rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                self.current_img_backup = self.current_img.copy()
                cv2.namedWindow(self.current_img_name)
                cv2.setMouseCallback(self.current_img_name, self.mark_key_points)

                key = None
                while True:
                    # display the image and wait for a keypress
                    cv2.imshow(self.current_img_name, self.current_img)
                    key = cv2.waitKey(1) & 0xFF

                    # if the 'r' key is pressed, reset the cropping region
                    if key == ord("r"):
                        self.current_img = self.current_img_backup.copy()

                    # if the 'o' key is pressed, record the selected key-point.
                    elif key == ord("o"):
                        if self.current_key_point:
                            self.key_points.append(self.current_key_point)
                            logger.debug(f'key points now: {self.key_points}')

                    # if the 'n' key is pressed, break from the loop and start specifying key-points of next image.
                    elif key == ord("n"):
                        self.db_upsert()
                        self.draw_map()
                        self.key_points = []
                        break

                    elif key == ord("f"):
                        break

                if key == ord("f"):
                    break

    def draw_map(self):
        """Method to create angular map with marked key points of the image.
        """
        middle_point = self.get_middle_point()

        for point in self.key_points:
            if point != middle_point:
                cv2.line(self.current_img, middle_point, point, (0, 255, 0), 1, cv2.LINE_AA)

        self.save_mapped_img()

    def save_mapped_img(self):
        """Method to save image after mapping process ended.
        """
        cv2.imwrite(f'{self.mapped_img_folder}/{self.current_img_name}', self.current_img)

    def get_middle_point(self):
        """Method to find and get point that middle of the image by other key points.
        """
        if self.key_points:
            img_height = self.current_img_backup.shape[0]
            img_width = self.current_img_backup.shape[1]

            middle_x = img_width / 2 + 1
            middle_y = img_height / 2 + 1

            middle_point = self.key_points[0]

            for point in self.key_points:
                if sqrt((point[0] - middle_x) ** 2 + (point[1] - middle_y) ** 2) < sqrt((middle_point[0] - middle_x) ** 2 + (middle_point[1] - middle_y) ** 2):
                    middle_point = point

            return middle_point

        return None

    def mark_key_points(self, event, x, y, flags, param):
        """Method to marking key-points on images in given dataset.
        """

        if event == cv2.EVENT_LBUTTONDOWN:

            if self.current_key_point:
                if self.current_key_point in self.key_points:
                    pass
                else:
                    self.current_img[self.current_key_point[1], self.current_key_point[0]] = self.current_img_backup[self.current_key_point[1], self.current_key_point[0]]

            self.current_key_point = (x, y)

        elif event == cv2.EVENT_LBUTTONUP:
            if not (x, y) == self.current_key_point:
                self.current_key_point = ()
            else:
                cv2.rectangle(self.current_img, self.current_key_point, self.current_key_point, (0, 255, 0), 2)
                cv2.imshow(self.current_img_name, self.current_img)

    def db_upsert(self, force_insert=False):
        """Function to insert(or update) the position to the database.

        Args:
            force_insert (bool):    Force insert flag.

        Returns:
            str:  Response.
        """

        if self.db.search((Query().name == self.current_img_name)):
            if force_insert:
                # self.already_exist = False
                self.db.update({'key_points': self.key_points}, Query().name == self.current_img_name)

            else:
                # self.already_exist = True
                return "Already Exist"
        else:
            self.db.insert({
                'name': self.current_img_name,
                'key_points': self.key_points
            })  # insert the given data

        return ""

    def __check_folders(self):
        """Method to checking the necessary folders created before. If not created creates them.
        """

        if not os.path.exists(self.out_folder):
            os.mkdir(self.out_folder)

        if not os.path.exists(self.mapped_img_folder):
            os.mkdir(self.mapped_img_folder)


