import enum
import numpy as np

from v2_dataset import units

_nan = float("nan")


class GratingConditions(enum.Enum):
    PLX_BEGIN = (None, 258, _nan, _nan, _nan, _nan, (_nan, _nan, _nan))
    PLX_START_STIMULUS = (None, 255, _nan, _nan, _nan, _nan, (_nan, _nan, _nan))
    PLX_STOP_STIMULUS = (None, 254, _nan, _nan, _nan, _nan, (_nan, _nan, _nan))
    PLX_END = (None, 259, _nan, _nan, _nan, _nan, (_nan, _nan, _nan))

    GRATING_1 = ("contrast varies", 1, 0.06, 1, 3, 0, (1.0, 1.0, 1.0))
    GRATING_2 = ("contrast varies", 2, 0.06, 1, 3, 45, (1.0, 1.0, 1.0))
    GRATING_3 = ("contrast varies", 3, 0.06, 1, 3, 90, (1.0, 1.0, 1.0))
    GRATING_4 = ("contrast varies", 4, 0.06, 1, 3, 135, (1.0, 1.0, 1.0))
    GRATING_5 = ("contrast varies", 5, 0.06, 1, 3, 180, (1.0, 1.0, 1.0))
    GRATING_6 = ("contrast varies", 6, 0.06, 1, 3, 225, (1.0, 1.0, 1.0))
    GRATING_7 = ("contrast varies", 7, 0.06, 1, 3, 270, (1.0, 1.0, 1.0))
    GRATING_8 = ("contrast varies", 8, 0.06, 1, 3, 315, (1.0, 1.0, 1.0))
    GRATING_9 = ("contrast varies", 9, 0.12, 1, 3, 0, (1.0, 1.0, 1.0))
    GRATING_10 = ("contrast varies", 10, 0.12, 1, 3, 45, (1.0, 1.0, 1.0))
    GRATING_11 = ("contrast varies", 11, 0.12, 1, 3, 90, (1.0, 1.0, 1.0))
    GRATING_12 = ("contrast varies", 12, 0.12, 1, 3, 135, (1.0, 1.0, 1.0))
    GRATING_13 = ("contrast varies", 13, 0.12, 1, 3, 180, (1.0, 1.0, 1.0))
    GRATING_14 = ("contrast varies", 14, 0.12, 1, 3, 225, (1.0, 1.0, 1.0))
    GRATING_15 = ("contrast varies", 15, 0.12, 1, 3, 270, (1.0, 1.0, 1.0))
    GRATING_16 = ("contrast varies", 16, 0.12, 1, 3, 315, (1.0, 1.0, 1.0))
    GRATING_17 = ("contrast varies", 17, 0.5, 1, 3, 0, (1.0, 1.0, 1.0))
    GRATING_18 = ("contrast varies", 18, 0.5, 1, 3, 45, (1.0, 1.0, 1.0))
    GRATING_19 = ("contrast varies", 19, 0.5, 1, 3, 90, (1.0, 1.0, 1.0))
    GRATING_20 = ("contrast varies", 20, 0.5, 1, 3, 135, (1.0, 1.0, 1.0))
    GRATING_21 = ("contrast varies", 21, 0.5, 1, 3, 180, (1.0, 1.0, 1.0))
    GRATING_22 = ("contrast varies", 22, 0.5, 1, 3, 225, (1.0, 1.0, 1.0))
    GRATING_23 = ("contrast varies", 23, 0.5, 1, 3, 270, (1.0, 1.0, 1.0))
    GRATING_24 = ("contrast varies", 24, 0.5, 1, 3, 315, (1.0, 1.0, 1.0))
    GRATING_25 = ("sf varies", 25, 1, 0.5, 3, 0, (1.0, 1.0, 1.0))
    GRATING_26 = ("sf varies", 26, 1, 0.5, 3, 45, (1.0, 1.0, 1.0))
    GRATING_27 = ("sf varies", 27, 1, 0.5, 3, 90, (1.0, 1.0, 1.0))
    GRATING_28 = ("sf varies", 28, 1, 0.5, 3, 135, (1.0, 1.0, 1.0))
    GRATING_29 = ("sf varies", 29, 1, 0.5, 3, 180, (1.0, 1.0, 1.0))
    GRATING_30 = ("sf varies", 30, 1, 0.5, 3, 225, (1.0, 1.0, 1.0))
    GRATING_31 = ("sf varies", 31, 1, 0.5, 3, 270, (1.0, 1.0, 1.0))
    GRATING_32 = ("sf varies", 32, 1, 0.5, 3, 315, (1.0, 1.0, 1.0))
    GRATING_33 = ("sf varies", 33, 1, 1, 3, 0, (1.0, 1.0, 1.0))
    GRATING_34 = ("sf varies", 34, 1, 1, 3, 45, (1.0, 1.0, 1.0))
    GRATING_35 = ("sf varies", 35, 1, 1, 3, 90, (1.0, 1.0, 1.0))
    GRATING_36 = ("sf varies", 36, 1, 1, 3, 135, (1.0, 1.0, 1.0))
    GRATING_37 = ("sf varies", 37, 1, 1, 3, 180, (1.0, 1.0, 1.0))
    GRATING_38 = ("sf varies", 38, 1, 1, 3, 225, (1.0, 1.0, 1.0))
    GRATING_39 = ("sf varies", 39, 1, 1, 3, 270, (1.0, 1.0, 1.0))
    GRATING_40 = ("sf varies", 40, 1, 1, 3, 315, (1.0, 1.0, 1.0))
    GRATING_41 = ("sf varies", 41, 1, 2, 3, 0, (1.0, 1.0, 1.0))
    GRATING_42 = ("sf varies", 42, 1, 2, 3, 45, (1.0, 1.0, 1.0))
    GRATING_43 = ("sf varies", 43, 1, 2, 3, 90, (1.0, 1.0, 1.0))
    GRATING_44 = ("sf varies", 44, 1, 2, 3, 135, (1.0, 1.0, 1.0))
    GRATING_45 = ("sf varies", 45, 1, 2, 3, 180, (1.0, 1.0, 1.0))
    GRATING_46 = ("sf varies", 46, 1, 2, 3, 225, (1.0, 1.0, 1.0))
    GRATING_47 = ("sf varies", 47, 1, 2, 3, 270, (1.0, 1.0, 1.0))
    GRATING_48 = ("sf varies", 48, 1, 2, 3, 315, (1.0, 1.0, 1.0))
    GRATING_49 = ("speed varies", 49, 1, 1, 1, 0, (1.0, 1.0, 1.0))
    GRATING_50 = ("speed varies", 50, 1, 1, 1, 45, (1.0, 1.0, 1.0))
    GRATING_51 = ("speed varies", 51, 1, 1, 1, 90, (1.0, 1.0, 1.0))
    GRATING_52 = ("speed varies", 52, 1, 1, 1, 135, (1.0, 1.0, 1.0))
    GRATING_53 = ("speed varies", 53, 1, 1, 1, 180, (1.0, 1.0, 1.0))
    GRATING_54 = ("speed varies", 54, 1, 1, 1, 225, (1.0, 1.0, 1.0))
    GRATING_55 = ("speed varies", 55, 1, 1, 1, 270, (1.0, 1.0, 1.0))
    GRATING_56 = ("speed varies", 56, 1, 1, 1, 315, (1.0, 1.0, 1.0))
    GRATING_57 = ("speed varies", 57, 1, 1, 10, 0, (1.0, 1.0, 1.0))
    GRATING_58 = ("speed varies", 58, 1, 1, 10, 45, (1.0, 1.0, 1.0))
    GRATING_59 = ("speed varies", 59, 1, 1, 10, 90, (1.0, 1.0, 1.0))
    GRATING_60 = ("speed varies", 60, 1, 1, 10, 135, (1.0, 1.0, 1.0))
    GRATING_61 = ("speed varies", 61, 1, 1, 10, 180, (1.0, 1.0, 1.0))
    GRATING_62 = ("speed varies", 62, 1, 1, 10, 225, (1.0, 1.0, 1.0))
    GRATING_63 = ("speed varies", 63, 1, 1, 10, 270, (1.0, 1.0, 1.0))
    GRATING_64 = ("speed varies", 64, 1, 1, 10, 315, (1.0, 1.0, 1.0))
    GRATING_65 = ("color varies", 65, 1, 1, 3, 0, (0, 42 / 255, 10 / 255))
    GRATING_66 = ("color varies", 66, 1, 1, 3, 45, (0, 42 / 255, 10 / 255))
    GRATING_67 = ("color varies", 67, 1, 1, 3, 90, (0, 42 / 255, 10 / 255))
    GRATING_68 = ("color varies", 68, 1, 1, 3, 135, (0, 42 / 255, 10 / 255))
    GRATING_69 = ("color varies", 69, 1, 1, 3, 180, (0, 42 / 255, 10 / 255))
    GRATING_70 = ("color varies", 70, 1, 1, 3, 225, (0, 42 / 255, 10 / 255))
    GRATING_71 = ("color varies", 71, 1, 1, 3, 270, (0, 42 / 255, 10 / 255))
    GRATING_72 = ("color varies", 72, 1, 1, 3, 315, (0, 42 / 255, 10 / 255))
    GRATING_73 = ("color varies", 73, 1, 1, 3, 0, (0, 42 / 255, 10 / 255))
    GRATING_74 = ("sf varies with speed", 74, 1, 0.5, 1.5, 45, (1.0, 1.0, 1.0))
    GRATING_75 = ("sf varies with speed", 75, 1, 0.5, 1.5, 90, (1.0, 1.0, 1.0))
    GRATING_76 = ("sf varies with speed", 76, 1, 0.5, 1.5, 135, (1.0, 1.0, 1.0))
    GRATING_77 = ("sf varies with speed", 77, 1, 0.5, 1.5, 180, (1.0, 1.0, 1.0))
    GRATING_78 = ("sf varies with speed", 78, 1, 0.5, 1.5, 225, (1.0, 1.0, 1.0))
    GRATING_79 = ("sf varies with speed", 79, 1, 0.5, 1.5, 270, (1.0, 1.0, 1.0))
    GRATING_80 = ("sf varies with speed", 80, 1, 0.5, 1.5, 315, (1.0, 1.0, 1.0))
    GRATING_81 = ("sf varies with speed", 81, 1, 0.5, 1.5, 0, (1.0, 1.0, 1.0))
    GRATING_82 = ("sf varies with speed", 82, 1, 2, 6, 45, (1.0, 1.0, 1.0))
    GRATING_83 = ("sf varies with speed", 83, 1, 2, 6, 90, (1.0, 1.0, 1.0))
    GRATING_84 = ("sf varies with speed", 84, 1, 2, 6, 135, (1.0, 1.0, 1.0))
    GRATING_85 = ("sf varies with speed", 85, 1, 2, 6, 180, (1.0, 1.0, 1.0))
    GRATING_86 = ("sf varies with speed", 86, 1, 2, 6, 225, (1.0, 1.0, 1.0))
    GRATING_87 = ("sf varies with speed", 87, 1, 2, 6, 270, (1.0, 1.0, 1.0))
    GRATING_88 = ("sf varies with speed", 88, 1, 2, 6, 315, (1.0, 1.0, 1.0))
    GRATING_89 = ("sf varies with speed", 89, 1, 2, 6, 0, (1.0, 1.0, 1.0))
    GRATING_90 = ("sf varies with speed", 90, 1, 4, 12, 45, (1.0, 1.0, 1.0))
    GRATING_91 = ("sf varies with speed", 91, 1, 4, 12, 90, (1.0, 1.0, 1.0))
    GRATING_92 = ("sf varies with speed", 92, 1, 4, 12, 135, (1.0, 1.0, 1.0))
    GRATING_93 = ("sf varies with speed", 93, 1, 4, 12, 180, (1.0, 1.0, 1.0))
    GRATING_94 = ("sf varies with speed", 94, 1, 4, 12, 225, (1.0, 1.0, 1.0))
    GRATING_95 = ("sf varies with speed", 95, 1, 4, 12, 270, (1.0, 1.0, 1.0))
    GRATING_96 = ("sf varies with speed", 96, 1, 4, 12, 315, (1.0, 1.0, 1.0))
    GRATING_97 = ("sf varies with speed", 97, 1, 4, 12, 0, (1.0, 1.0, 1.0))
    GRATING_98 = ("sf varies with speed", 98, 1, 1, 30, 45, (1.0, 1.0, 1.0))
    GRATING_99 = ("sf varies with speed", 99, 1, 1, 30, 90, (1.0, 1.0, 1.0))
    GRATING_100 = ("sf varies with speed", 100, 1, 1, 30, 135, (1.0, 1.0, 1.0))
    GRATING_101 = ("sf varies with speed", 101, 1, 1, 30, 180, (1.0, 1.0, 1.0))
    GRATING_102 = ("sf varies with speed", 102, 1, 1, 30, 225, (1.0, 1.0, 1.0))
    GRATING_103 = ("sf varies with speed", 103, 1, 1, 30, 270, (1.0, 1.0, 1.0))
    GRATING_104 = ("sf varies with speed", 104, 1, 1, 30, 315, (1.0, 1.0, 1.0))
    GRATING_105 = ("sf varies with speed", 105, 1, 1, 30, 0, (1.0, 1.0, 1.0))

    @classmethod
    def as_array(cls, sf_unit="1/radian", tf_unit="hertz", orient_unit="radian"):
        return np.array(
            [
                (
                    c.group,
                    c.value,
                    c.contrast,
                    c.spatial_frequency.to(sf_unit).m,
                    c.temporal_frequency.to(tf_unit).m,
                    c.orientation.to(orient_unit),
                    c.color,
                )
                for c in cls
                if "GRATING" in c.name
            ],
            dtype=[
                ("group", "U20"),
                ("code", "u2"),
                ("contrast", "f4"),
                ("sf", "f4"),
                ("tf", "f4"),
                ("orient", "f4"),
                ("color", "(3,)f4"),
            ],
        )

    @classmethod
    def condition_groups(cls):
        return {
            "contrast varies": [cls[f"GRATING_{i}"] for i in range(1, 25)],
            "sf varies": [cls[f"GRATING_{i}"] for i in range(25, 49)],
            "speed varies": [cls[f"GRATING_{i}"] for i in range(49, 65)],
            "color varies": [cls[f"GRATING_{i}"] for i in range(65, 74)],
            "sf varies with speed": [cls[f"GRATING_{i}"] for i in range(74, 106)],
        }

    def __new__(
        cls,
        group,
        code,
        contrast,
        spatial_frequency,
        temporal_frequency,
        orientation,
        color,
    ):
        obj = object.__new__(cls)
        obj._value_ = code
        obj.group = group
        obj.contrast = contrast
        obj.spatial_frequency = spatial_frequency / units.degree
        obj.temporal_frequency = temporal_frequency / units.second
        obj.orientation = orientation * units.degree
        obj.color = color
        return obj

    @property
    def is_colored(self):
        return self.color != (1.0, 1.0, 1.0)


class MovingBarConditions(enum.Enum):
    PLX_BEGIN = (258, _nan)
    PLX_START_STIMULUS = (255, _nan)
    PLX_STOP_STIMULUS = (254, _nan)
    PLX_END = (259, _nan)

    MB_1 = (1, 0)
    MB_2 = (2, 45)
    MB_3 = (3, 90)
    MB_4 = (4, 135)
    MB_5 = (5, 180)
    MB_6 = (6, 235)
    MB_7 = (7, 270)
    MB_8 = (8, 315)

    def __new__(cls, code, orientation):
        obj = object.__new__(cls)
        obj._value_ = code
        obj.orientation = orientation * units.deg
        return obj


class Stimulus(enum.Enum):
    """This enumeration describes known stimulus values in the dataset.

    .. attribute:: conditions_type type

        Maps to an enumeration type in this module (*e.g.* :class:`MovingBarConditions`, or :class:`GratingConditions`)
        that describes the experimental conditions for the corresponding stimulus type.
    """

    BLACK = ("BLACK", None)
    BLACK_1 = ("BLACK_1", None)
    BLACK_68 = ("BLACK_68", None)
    BLACK_COL = ("BLACK_COL", None)
    BLACK_COL_1 = ("BLACK_COL_1", None)
    COL = ("COL", None)
    COL_1 = ("COL_1", None)
    COL_68 = ("COL_68", None)
    CON = ("CON", None)
    CONTRAST = ("CONTRAST", None)
    CON_1 = ("CON_1", None)
    CON_68 = ("CON_68", None)
    ELETRO = ("ELETRO", None)
    GRATING = ("GRATING", GratingConditions)
    MB = ("MB", MovingBarConditions)

    def __new__(cls, name, conditions_type):
        obj = object.__new__(cls)
        obj._value_ = name
        obj.conditions_type = conditions_type
        return obj

    def conditions(self, stimulus_only=False):
        return [
            cond
            for cond in self.conditions_type
            if not (stimulus_only and "PLX" in cond.name)
        ]

    def no_conditions(self, stimulus_only=False):
        return len(self.conditions_type) - int(stimulus_only) * 4
