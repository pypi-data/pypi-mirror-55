import six

from descarteslabs import scenes

from ... import env
from ...cereal import serializable
from ..containers import Dict, KnownDict, Struct, Tuple, List
from ..core import typecheck_promote, _resolve_lambdas
from ..datetimes import Datetime
from ..primitives import Any, Bool, Float, Int, Str, NoneType
from .feature import Feature
from .featurecollection import FeatureCollection
from .geometry import Geometry
from .mixins import BandsMixin


def _DelayedImageCollection():
    from .imagecollection import ImageCollection

    return ImageCollection


ImageBase = Struct[
    {
        "properties": KnownDict[
            {
                "id": Str,
                "date": Datetime,
                "product": Str,
                "crs": Str,
                "geotrans": Tuple[Float, Float, Float, Float, Float, Float],
            },
            Str,
            Any,
        ],
        "bandinfo": Dict[
            Str,
            KnownDict[
                {
                    "id": Str,
                    "name": Str,
                    # "unit": Str,
                    "data_range": Tuple[Float, Float],
                    # "physical_range": Tuple[Float, Float],
                },
                Str,
                Any,
            ],
        ],
    }
]


@serializable(is_named_concrete_type=True)
class Image(ImageBase, BandsMixin):
    """
    Proxy Image; construct with `~.Image.from_id` or `~.Image.from_scenes`.

    An Image is a proxy object holding multiple (ordered) bands of raster data,
    plus some metadata.

    Images don't have a set spatial extent, CRS, resolution, etc:
    that's determined at computation time by the `~.geospatial.GeoContext` passsed in.
    """

    _doc = {
        "properties": """\
            Metadata for the `Image`.

            ``properties`` is a `Dict` which always contains these fields:

            * ``id`` (`.Str`): the Descartes Labs ID of the Image
            * ``product`` (`.Str`): the Descartes Labs ID of the product the Image belogs to
            * ``date`` (`.Datetime`): the UTC date the Image was acquired
            * ``crs`` (`.Str`): the original Coordinate Reference System of the Image
            * ``geotrans`` (`.Tuple`): The original 6-tuple GDAL geotrans for the Image.

            Accessing other fields will return instances of `.Any`.
            Accessing fields that don't actually exist on the data is a compute-time error.

            Example
            -------
            >>> import descarteslabs.workflows as wf
            >>> img = wf.Image.from_id("landsat:LC08:PRE:TOAR:meta_LC80270312016188_v1")
            >>> img.properties['date']
            <descarteslabs.workflows.types.datetimes.datetime_.Datetime object at 0x...>
            >>> img.properties['date'].year
            <descarteslabs.workflows.types.primitives.number.Int object at 0x...>
            >>> img.properties['id']
            <descarteslabs.workflows.types.primitives.string.Str object at 0x...>
            >>> img.properties['foobar']  # almost certainly a compute-time error
            <descarteslabs.workflows.types.primitives.any_.Any object at 0x...>
            """,
        "bandinfo": """\
            Metadata about the bands of the `Image`.

            ``bandinfo`` is a `Dict`, where keys are band names and values are Dicts
            which always contain these fields:

            * ``id`` (`.Str`): the Descartes Labs ID of the band
            * ``name`` (`.Str`): the name of the band. Equal to the key the Dict
              is stored under in ``bandinfo``
            * ``data_range`` (`.Tuple`): The ``(min, max)`` values the original data had.
              However, data in Images is automatically rescaled to physical range,
              or ``[0, 1]`` if physical range is undefined, so it won't be in ``data_range``
              anymore.

            Accessing other fields will return instances of `.Any`.
            Accessing fields that don't actually exist on the data is a compute-time error.

            Example
            -------
            >>> import descarteslabs.workflows as wf
            >>> img = wf.Image.from_id("landsat:LC08:PRE:TOAR:meta_LC80270312016188_v1")
            >>> img.bandinfo['red']['data_range']
            <descarteslabs.workflows.types.containers.tuple_.Tuple[Float, Float] object at 0x...>
            >>> img.bandinfo['red']['foobar']  # almost certainly a compute-time error
            <descarteslabs.workflows.types.primitives.any_.Any object at 0x...>
            >>> img.bandinfo['foobar']['id']  # also likely a compute-time error
            <descarteslabs.workflows.types.primitives.string.Str object at 0x...>
            """,
    }

    def __init__(self):
        raise TypeError(
            "Please use a classmethod such as `Image.from_id` or `Image.from_scene` to instantiate an Image."
        )

    @classmethod
    def _promote(cls, obj):
        if isinstance(obj, scenes.Scene):
            return cls.from_scene(obj)
        return super(Image, cls)._promote(obj)

    @classmethod
    @typecheck_promote(Str)
    def from_id(cls, image_id, resampler=None, processing_level=None):
        """
        Create a proxy `Image` from an ID in the Descartes Labs catalog.

        Parameters
        ----------
        image_id: Str
            ID of the image
        resampler: str, optional, default None
            Algorithm used to interpolate pixel values when scaling and transforming
            the image to the resolution and CRS eventually defined by a `~.geospatial.GeoContext`.
            Possible values are ``near`` (nearest-neighbor), ``bilinear``, ``cubic``, ``cubicsplice``,
            ``lanczos``, ``average``, ``mode``, ``max``, ``min``, ``med``, ``q1``, ``q3``.
        processing_level : str, optional
            Reflectance processing level. Possible values are ``'toa'`` (top of atmosphere)
            and ``'surface'``. For products that support it, ``'surface'`` applies
            Descartes Labs' general surface reflectance algorithm to the output.

        Returns
        -------
        img: ~.geospatial.Image
        """
        if resampler is not None and resampler not in [
            "near",
            "bilinear",
            "cubic",
            "cubicsplice",
            "lanczos",
            "average",
            "mode",
            "max",
            "min",
            "med",
            "q1",
            "q3",
        ]:
            raise ValueError("Unknown resampler type: {}".format(resampler))
        if processing_level is not None and processing_level not in ("toa", "surface"):
            raise ValueError(
                "Unknown processing level: {!r}. Must be None, 'toa', or 'surface'.".format(
                    processing_level
                )
            )
        return cls._from_apply(
            "Image.load",
            image_id,
            geocontext=env.geoctx,
            token=env._token,
            resampler=resampler,
            processing_level=processing_level,
        )

    @classmethod
    def from_scene(cls, scene):
        "Create a proxy image from a `~descarteslabs.scenes.scene.Scene` object"
        return cls.from_id(scene.properties["id"])

    @typecheck_promote(lambda: Image)
    def concat_bands(self, other_image):
        """
        New `Image`, with the bands in ``other_image`` appended to this one.

        If band names overlap, the band from the *other* `Image` will be suffixed with "_1".
        """
        return self._from_apply("Image.concat_bands", self, other_image)

    @typecheck_promote(
        (lambda: Image, Geometry, Feature, FeatureCollection), replace=Bool
    )
    def mask(self, mask, replace=False):
        """
        New `Image`, masked with a boolean `Image` or vector object.

        Parameters
        ----------
        mask: `Image`, `Geometry`, `~.workflows.types.geospatial.Feature`, `~.workflows.types.geospatial.FeatureCollection`
            A single-band `Image` of boolean values,
            (such as produced by ``img > 2``, for example)
            where True means masked (invalid).

            Or, a vector (`Geometry`, `~.workflows.types.geospatial.Feature`,
            or `~.workflows.types.geospatial.FeatureCollection`),
            in which case pixels *outside* the vector are masked.
        replace: Bool, default False
            If False (default), adds this mask to the current one,
            so already-masked pixels remain masked,
            or replaces the current mask with this new one if True.
        """  # noqa
        if isinstance(mask, (Geometry, Feature, FeatureCollection)):
            mask = mask.rasterize().getmask()
        return self._from_apply("mask", self, mask, replace=replace)

    def getmask(self):
        "Mask of this `Image`, as a new `Image` with one boolean band named ``'mask'``"
        return self._from_apply("getmask", self)

    def colormap(self, named_colormap="viridis", vmin=None, vmax=None):
        """
        Apply a colormap to an `Image`. Image must have a single band.

        Parameters
        ----------
        named_colormap: str, default "viridis"
            The name of the Colormap registered with matplotlib.
            See https://matplotlib.org/users/colormaps.html for colormap options.
        vmin: float, default None
            The minimum value of the range to normalize the bands within.
            If specified, vmax must be specified as well.
        vmax: float, default None
            The maximum value of the range to normalize the bands within.
            If specified, vmin must be specified as well.

        Note: If neither vmin nor vmax are specified, the min and max values in the `Image` will be used.
        """
        if (vmin is not None and vmax is None) or (vmin is None and vmax is not None):
            raise ValueError("Must specify both vmin and vmax, or neither.")
        if named_colormap not in [
            "viridis",
            "plasma",
            "inferno",
            "magma",
            "cividis",
            "Greys",
            "Purples",
            "Blues",
            "Greens",
            "Oranges",
            "Reds",
            "YlOrBr",
            "YlOrRd",
            "OrRd",
            "PuRd",
            "RdPu",
            "BuPu",
            "GnBu",
            "PuBu",
            "YlGnBu",
            "PuBuGn",
            "BuGn",
            "YlGn",
            "binary",
            "gist_yarg",
            "gist_gray",
            "gray",
            "bone",
            "pink",
            "spring",
            "summer",
            "autumn",
            "winter",
            "cool",
            "Wistia",
            "hot",
            "afmhot",
            "gist_heat",
            "copper",
            "PiYG",
            "PRGn",
            "BrBG",
            "PuOr",
            "RdGy",
            "RdBu",
            "RdYlBu",
            "RdYlGn",
            "Spectral",
            "coolwarm",
            "bwr",
            "seismic",
            "twilight",
            "twilight_shifted",
            "hsv",
            "Pastel1",
            "Pastel2",
            "Paired",
            "Accent",
            "Dark2",
            "Set1",
            "Set2",
            "Set3",
            "tab10",
            "tab20",
            "tab20b",
            "tab20c",
            "flag",
            "prism",
            "ocean",
            "gist_earth",
            "terrain",
            "gist_stern",
            "gnuplot",
            "gnuplot2",
            "CMRmap",
            "cubehelix",
            "brg",
            "gist_rainbow",
            "rainbow",
            "jet",
            "nipy_spectral",
            "gist_ncar",
        ]:
            raise ValueError("Unknown colormap type: {}".format(named_colormap))
        return self._from_apply("colormap", self, named_colormap, vmin, vmax)

    _STATS_RETURN_TYPES = {
        None: Float,
        "pixels": Dict[Str, Float],
        "bands": lambda: Image,
        ("pixels", "bands"): Float,
        ("bands", "pixels"): Float,
    }
    _RESOLVED_STATS_RETURN_TYPES = None

    @classmethod
    def _stats_return_type(cls, axis):
        if cls._RESOLVED_STATS_RETURN_TYPES is None:
            cls._RESOLVED_STATS_RETURN_TYPES = _resolve_lambdas(cls._STATS_RETURN_TYPES)

        try:
            return cls._RESOLVED_STATS_RETURN_TYPES[axis]
        except KeyError:
            raise ValueError(
                "Invalid axis argument {!r}, should be one of {}.".format(
                    axis,
                    ", ".join(
                        map(repr, six.viewkeys(cls._RESOLVED_STATS_RETURN_TYPES))
                    ),
                )
            )

    def min(self, axis=None):
        """
        Minimum pixel value across the provided ``axis``, or across all pixels in the image
        if no ``axis`` argument is provided.

        Parameters
        ----------
        axis: {None, "pixels", "bands"}
            A Python string indicating the axis along which to take the minimum.

            Options:

            * ``"pixels"``: Returns a ``Dict[Str, Float]`` of each band's minimum pixel value.
            * ``"bands"``: Returns a new `.Image` with
              one band, ``"min"``, containing the minimum value for each pixel across
              all bands.
            * ``None``: Returns a `.Float` that represents the minimum pixel value of the
              entire image.

        Returns
        -------
        ``Dict[Str, Float]`` or `.Image` or `.Float`
            Minimum pixel values across the provided ``axis``.  See the options for the ``axis``
            argument for details.

        Example
        -------
        >>> import descarteslabs.workflows as wf
        >>> img = wf.Image.from_id("landsat:LC08:01:RT:TOAR:meta_LC08_L1TP_033035_20170516_20170516_01_RT_v1")
        >>> min_img = img.min(axis="bands")
        >>> band_mins = img.min(axis="pixels")
        >>> min_pixel = img.min(axis=None)
        """
        return_type = self._stats_return_type(axis)
        return return_type._from_apply("min", self, axis)

    def max(self, axis=None):
        """
        Maximum pixel value across the provided ``axis``, or across all pixels in the image
        if no ``axis`` argument is provided.

        Parameters
        ----------
        axis: {None, "pixels", "bands"}
            A Python string indicating the axis along which to take the maximum.

            Options:

            * ``"pixels"``: Returns a ``Dict[Str, Float]`` of each band's maximum pixel value.
            * ``"bands"``: Returns a new `.Image` with
              one band, ``"max"``, containing the maximum value for each pixel across
              all bands.
            * ``None``: Returns a `.Float` that represents the maximum pixel value of the
              entire image.

        Returns
        -------
        ``Dict[Str, Float]`` or `.Image` or `.Float`
            Maximum pixel values across the provided ``axis``.  See the options for the ``axis``
            argument for details.

        Example
        -------
        >>> import descarteslabs.workflows as wf
        >>> img = wf.Image.from_id("landsat:LC08:01:RT:TOAR:meta_LC08_L1TP_033035_20170516_20170516_01_RT_v1")
        >>> max_img = img.max(axis="bands")
        >>> band_maxs = img.max(axis="pixels")
        >>> max_pixel = img.max(axis=None)
        """
        return_type = self._stats_return_type(axis)
        return return_type._from_apply("max", self, axis)

    def mean(self, axis=None):
        """
        Mean pixel value across the provided ``axis``, or across all pixels in the image
        if no ``axis`` argument is provided.

        Parameters
        ----------
        axis: {None, "pixels", "bands"}
            A Python string indicating the axis along which to take the mean.

            Options:

            * ``"pixels"``: Returns a ``Dict[Str, Float]`` of each band's mean pixel value.
            * ``"bands"``: Returns a new `.Image` with
              one band, ``"mean"``, containing the mean value for each pixel across all
              bands.
            * ``None``: Returns a `.Float` that represents the mean pixel value of the entire
              image.

        Returns
        -------
        ``Dict[Str, Float]`` or `.Image` or `.Float`
            Mean pixel values across the provided ``axis``.  See the options for the ``axis``
            argument for details.

        Example
        -------
        >>> import descarteslabs.workflows as wf
        >>> img = wf.Image.from_id("landsat:LC08:01:RT:TOAR:meta_LC08_L1TP_033035_20170516_20170516_01_RT_v1")
        >>> mean_img = img.mean(axis="bands")
        >>> band_means = img.mean(axis="pixels")
        >>> mean_pixel = img.mean(axis=None)
        """
        return_type = self._stats_return_type(axis)
        return return_type._from_apply("mean", self, axis)

    def median(self, axis=None):
        """
        Median pixel value across the provided ``axis``, or across all pixels in the image
        if no ``axis`` argument is provided.

        Parameters
        ----------
        axis: {None, "pixels", "bands"}
            A Python string indicating the axis along which to take the median.

            Options:

            * ``"pixels"``: Returns a ``Dict[Str, Float]`` of each band's median pixel value.
            * ``"bands"``: Returns a new `.Image` with
              one band, ``"median"``, containing the median value for each pixel across
              all bands.
            * ``None``: Returns a `.Float` that represents the median pixel value of the
              entire image.

        Returns
        -------
        ``Dict[Str, Float]`` or `.Image` or `.Float`
            Median pixel values across the provided ``axis``.  See the options for the ``axis``
            argument for details.

        Example
        -------
        >>> import descarteslabs.workflows as wf
        >>> img = wf.Image.from_id("landsat:LC08:01:RT:TOAR:meta_LC08_L1TP_033035_20170516_20170516_01_RT_v1")
        >>> median_img = img.median(axis="bands")
        >>> band_medians = img.median(axis="pixels")
        >>> median_pixel = img.median(axis=None)
        """
        return_type = self._stats_return_type(axis)
        return return_type._from_apply("median", self, axis)

    def sum(self, axis=None):
        """
        Sum of pixel values across the provided ``axis``, or across all pixels in the image
        if no ``axis`` argument is provided.

        Parameters
        ----------
        axis: {None, "pixels", "bands"}
            A Python string indicating the axis along which to take the sum.

            Options:

            * ``"pixels"``: Returns a ``Dict[Str, Float]`` containing the sum of the pixel
              values for each band.
            * ``"bands"``: Returns a new `.Image` with
              one band, ``"sum"``, containing the sum across all bands for each pixel.
            * ``None``: Returns a `.Float` that represents the sum of all pixels in the
              image.

        Returns
        -------
        ``Dict[Str, Float]`` or `.Image` or `.Float`
            Sum of pixel values across the provided ``axis``.  See the options for the ``axis``
            argument for details.

        Example
        -------
        >>> import descarteslabs.workflows as wf
        >>> img = wf.Image.from_id("landsat:LC08:01:RT:TOAR:meta_LC08_L1TP_033035_20170516_20170516_01_RT_v1")
        >>> sum_img = img.sum(axis="bands")
        >>> band_sums = img.sum(axis="pixels")
        >>> sum_pixels = img.sum(axis=None)
        """
        return_type = self._stats_return_type(axis)
        return return_type._from_apply("sum", self, axis)

    def std(self, axis=None):
        """
        Standard deviation along the provided ``axis``, or across all pixels in the image
        if no ``axis`` argument is provided.

        Parameters
        ----------
        axis: {None, "pixels", "bands"}
            A Python string indicating the axis along which to take the standard deviation.

            Options:

            * ``"pixels"``: Returns a ``Dict[Str, Float]`` containing the standard deviation
              across each band.
            * ``"bands"``: Returns a new `.Image` with
              one band, ``"std"``, containing the standard deviation across all bands
              for each pixel.
            * ``None``: Returns a `.Float` that represents the standard deviation of the
              entire image.

        Returns
        -------
        ``Dict[Str, Float]`` or `.Image` or `.Float`
            Standard deviation along the provided ``axis``.  See the options for the ``axis``
            argument for details.

        Example
        -------
        >>> import descarteslabs.workflows as wf
        >>> img = wf.Image.from_id("landsat:LC08:01:RT:TOAR:meta_LC08_L1TP_033035_20170516_20170516_01_RT_v1")
        >>> std_img = img.std(axis="bands")
        >>> band_stds = img.std(axis="pixels")
        >>> std = img.std(axis=None)
        """
        return_type = self._stats_return_type(axis)
        return return_type._from_apply("std", self, axis)

    def count(self, axis=None):
        """
        Count of valid (unmasked) pixels across the provided ``axis``, or across all pixels
        in the image if no ``axis`` argument is provided.

        Parameters
        ----------
        axis: {None, "pixels", "bands"}
            A Python string indicating the axis along which to take the valid pixel count.

            Options:

            * ``"pixels"``: Returns a ``Dict[Str, Float]`` containing the count of valid
              pixels in each band.
            * ``"bands"``: Returns a new `.Image` with
              one band, ``"count"``, containing the count of valid pixels across all
              bands, for each pixel.
            * ``None``: Returns a `.Float` that represents the count of valid pixels in the
              image.

        Returns
        -------
        ``Dict[Str, Float]`` or `.Image` or `.Float`
            Count of valid pixels across the provided ``axis``.  See the options for the ``axis``
            argument for details.

        Example
        -------
        >>> import descarteslabs.workflows as wf
        >>> img = wf.Image.from_id("landsat:LC08:01:RT:TOAR:meta_LC08_L1TP_033035_20170516_20170516_01_RT_v1")
        >>> count_img = img.count(axis="bands")
        >>> band_counts = img.count(axis="pixels")
        >>> count = img.count(axis=None)
        """
        return_type = self._stats_return_type(axis)
        return return_type._from_apply("count", self, axis)

    # Binary comparators
    @typecheck_promote((lambda: Image, lambda: _DelayedImageCollection(), Int, Float))
    def __lt__(self, other):
        return _result_type(other)._from_apply("lt", self, other)

    @typecheck_promote((lambda: Image, lambda: _DelayedImageCollection(), Int, Float))
    def __le__(self, other):
        return _result_type(other)._from_apply("le", self, other)

    @typecheck_promote(
        (lambda: Image, lambda: _DelayedImageCollection(), Int, Float, Bool)
    )
    def __eq__(self, other):
        return _result_type(other)._from_apply("eq", self, other)

    @typecheck_promote(
        (lambda: Image, lambda: _DelayedImageCollection(), Int, Float, Bool)
    )
    def __ne__(self, other):
        return _result_type(other)._from_apply("ne", self, other)

    @typecheck_promote((lambda: Image, lambda: _DelayedImageCollection(), Int, Float))
    def __gt__(self, other):
        return _result_type(other)._from_apply("gt", self, other)

    @typecheck_promote((lambda: Image, lambda: _DelayedImageCollection(), Int, Float))
    def __ge__(self, other):
        return _result_type(other)._from_apply("ge", self, other)

    # Bitwise operators
    def __invert__(self):
        return self._from_apply("invert", self)

    @typecheck_promote((lambda: Image, lambda: _DelayedImageCollection(), Int, Bool))
    def __and__(self, other):
        return _result_type(other)._from_apply("and", self, other)

    @typecheck_promote((lambda: Image, lambda: _DelayedImageCollection(), Int, Bool))
    def __or__(self, other):
        return _result_type(other)._from_apply("or", self, other)

    @typecheck_promote((lambda: Image, lambda: _DelayedImageCollection(), Int, Bool))
    def __xor__(self, other):
        return _result_type(other)._from_apply("xor", self, other)

    @typecheck_promote((lambda: Image, lambda: _DelayedImageCollection(), Int))
    def __lshift__(self, other):
        return _result_type(other)._from_apply("lshift", self, other)

    @typecheck_promote((lambda: Image, lambda: _DelayedImageCollection(), Int))
    def __rshift__(self, other):
        return _result_type(other)._from_apply("rshift", self, other)

    # Reflected bitwise operators
    @typecheck_promote((lambda: Image, lambda: _DelayedImageCollection(), Int, Bool))
    def __rand__(self, other):
        return _result_type(other)._from_apply("rand", self, other)

    @typecheck_promote((lambda: Image, lambda: _DelayedImageCollection(), Int, Bool))
    def __ror__(self, other):
        return _result_type(other)._from_apply("ror", self, other)

    @typecheck_promote((lambda: Image, lambda: _DelayedImageCollection(), Int, Bool))
    def __rxor__(self, other):
        return _result_type(other)._from_apply("rxor", self, other)

    @typecheck_promote((lambda: Image, lambda: _DelayedImageCollection(), Int))
    def __rlshift__(self, other):
        return _result_type(other)._from_apply("rlshift", self, other)

    @typecheck_promote((lambda: Image, lambda: _DelayedImageCollection(), Int))
    def __rrshift__(self, other):
        return _result_type(other)._from_apply("rrshift", self, other)

    # Arithmetic operators
    def log(img):
        "Element-wise natural log of an `Image`"
        from ..math import arithmetic

        return arithmetic.log(img)

    def log2(img):
        "Element-wise base 2 log of an `Image`"
        from ..math import arithmetic

        return arithmetic.log2(img)

    def log10(img):
        "Element-wise base 10 log of an `Image`"
        from ..math import arithmetic

        return arithmetic.log10(img)

    def sqrt(self):
        "Element-wise square root of an `Image`"
        from ..math import arithmetic

        return arithmetic.sqrt(self)

    def cos(self):
        "Element-wise cosine of an `Image`"
        from ..math import arithmetic

        return arithmetic.cos(self)

    def sin(self):
        "Element-wise sine of an `Image`"
        from ..math import arithmetic

        return arithmetic.sin(self)

    def tan(self):
        "Element-wise tangent of an `Image`"
        from ..math import arithmetic

        return arithmetic.tan(self)

    @typecheck_promote(
        (Int, Float, NoneType, List[Int], List[Float], List[NoneType]),
        (Int, Float, NoneType, List[Int], List[Float], List[NoneType]),
    )
    def clip_values(self, min=None, max=None):
        """
        Given an interval, band values outside the interval are clipped to the interval edge.

        Parameters
        ----------
        min: float or list, default None
            Minimum value of clipping interval. If None, clipping is not performed on the lower interval edge.
        max: float or list, default None
            Maximum value of clipping interval. If None, clipping is not performed on the upper interval edge.
            Different per-band clip values can by given by using lists for ``min`` or ``max``,
            in which case they must be the same length as the number of bands.

        Note: ``min`` and ``max`` cannot both be None. At least one must be specified.
        """
        if min is None and max is None:
            raise ValueError(
                "min and max cannot both be None. At least one must be specified."
            )
        return self._from_apply("clip_values", self, min, max)

    def scale_values(self, range_min, range_max, domain_min=None, domain_max=None):
        """
        Given an interval, band values will be scaled to the interval.

        Parameters
        ----------
        range_min: float
            Minimum value of output range..
        range_max: float
            Maximum value of output range.
        domain_min: float, default None
            Minimum value of the domain. If None, the band minimim is used.
        domain_max: float, default None
            Maximum value of the domain. If None, the band maximum is used.
        """
        return self._from_apply(
            "scale_values", self, range_min, range_max, domain_min, domain_max
        )

    def __neg__(self):
        return self._from_apply("neg", self)

    def __pos__(self):
        return self._from_apply("pos", self)

    def __abs__(self):
        return self._from_apply("abs", self)

    @typecheck_promote(
        (lambda: Image, lambda: _DelayedImageCollection(), Int, Float), _reflect=True
    )
    def __add__(self, other):
        return _result_type(other)._from_apply("add", self, other)

    @typecheck_promote((lambda: Image, lambda: _DelayedImageCollection(), Int, Float), _reflect=True)
    def __sub__(self, other):
        return _result_type(other)._from_apply("sub", self, other)

    @typecheck_promote((lambda: Image, lambda: _DelayedImageCollection(), Int, Float), _reflect=True)
    def __mul__(self, other):
        return _result_type(other)._from_apply("mul", self, other)

    @typecheck_promote((lambda: Image, lambda: _DelayedImageCollection(), Int, Float), _reflect=True)
    def __div__(self, other):
        return _result_type(other)._from_apply("div", self, other)

    @typecheck_promote((lambda: Image, lambda: _DelayedImageCollection(), Int, Float), _reflect=True)
    def __truediv__(self, other):
        return _result_type(other)._from_apply("div", self, other)

    @typecheck_promote((lambda: Image, lambda: _DelayedImageCollection(), Int, Float), _reflect=True)
    def __floordiv__(self, other):
        return _result_type(other)._from_apply("floordiv", self, other)

    @typecheck_promote((lambda: Image, lambda: _DelayedImageCollection(), Int, Float), _reflect=True)
    def __mod__(self, other):
        return _result_type(other)._from_apply("mod", self, other)

    @typecheck_promote((lambda: Image, lambda: _DelayedImageCollection(), Int, Float), _reflect=True)
    def __pow__(self, other):
        return _result_type(other)._from_apply("pow", self, other)

    # Reflected arithmetic operators
    @typecheck_promote((lambda: Image, lambda: _DelayedImageCollection(), Int, Float))
    def __radd__(self, other):
        return _result_type(other)._from_apply("radd", self, other)

    @typecheck_promote((lambda: Image, lambda: _DelayedImageCollection(), Int, Float))
    def __rsub__(self, other):
        return _result_type(other)._from_apply("rsub", self, other)

    @typecheck_promote((lambda: Image, lambda: _DelayedImageCollection(), Int, Float))
    def __rmul__(self, other):
        return _result_type(other)._from_apply("rmul", self, other)

    @typecheck_promote((lambda: Image, lambda: _DelayedImageCollection(), Int, Float))
    def __rdiv__(self, other):
        return _result_type(other)._from_apply("rdiv", self, other)

    @typecheck_promote((lambda: Image, lambda: _DelayedImageCollection(), Int, Float))
    def __rtruediv__(self, other):
        return _result_type(other)._from_apply("rtruediv", self, other)

    @typecheck_promote((lambda: Image, lambda: _DelayedImageCollection(), Int, Float))
    def __rfloordiv__(self, other):
        return _result_type(other)._from_apply("rfloordiv", self, other)

    @typecheck_promote((lambda: Image, lambda: _DelayedImageCollection(), Int, Float))
    def __rmod__(self, other):
        return _result_type(other)._from_apply("rmod", self, other)

    @typecheck_promote((lambda: Image, lambda: _DelayedImageCollection(), Int, Float))
    def __rpow__(self, other):
        return _result_type(other)._from_apply("rpow", self, other)

    def tile_layer(self, name=None, scales=None, colormap=None, checkerboard=True, **parameters):
        """
        A `.WorkflowsLayer` for this `Image`.

        Generally, use `Image.visualize` for displaying on map.
        Only use this method if you're managing your own ipyleaflet Map instances,
        and creating more custom visualizations.

        Parameters
        ----------
        name: str
            The name of the layer.
        scales: list of lists, default None
            The scaling to apply to each band in the `Image`.

            If `Image` contains 3 bands, ``scales`` must be a list like ``[(0, 1), (0, 1), (-1, 1)]``.

            If `Image` contains 1 band, ``scales`` must be a list like ``[(0, 1)]``,
            or just ``(0, 1)`` for convenience

            If None, each 256x256 tile will be scaled independently.
            based on the min and max values of its data.
        colormap: str, default None
            The name of the colormap to apply to the `Image`. Only valid if the `Image` has a single band.
        checkerboard: bool, default True
            Whether to display a checkerboarded background for missing or masked data.
        **parameters: JSON-serializable value, Proxytype, or ipywidgets.Widget
            Runtime parameters to use when computing tiles.
            Values can be any JSON-serializable value, a `Proxytype` instance, or an ipywidgets ``Widget``.

            See the docstring for `visualize` for more detail.

        Returns
        -------
        layer: `.WorkflowsLayer`
        """
        from ... import interactive

        layer = interactive.WorkflowsLayer(self, name=name, parameters=parameters)
        layer.set_scales(scales, new_colormap=colormap)
        layer.checkerboard = checkerboard

        return layer

    def visualize(self, name, scales=None, colormap=None, checkerboard=True, map=None, **parameters):
        """
        Add this `Image` to `wf.map <.interactive.map>`, or replace a layer with the same name.

        Parameters
        ----------
        name: str
            The name of the layer.

            If a layer with this name already exists on `wf.map <.interactive.map>`,
            it will be replaced with this `Image`, scales, and colormap.
            This allows you to re-run cells in Jupyter calling `visualize`
            without adding duplicate layers to the map.
        scales: list of lists, default None
            The scaling to apply to each band in the `Image`.

            If `Image` contains 3 bands, ``scales`` must be a list like ``[(0, 1), (0, 1), (-1, 1)]``.

            If `Image` contains 1 band, ``scales`` must be a list like ``[(0, 1)]``,
            or just ``(0, 1)`` for convenience

            If None, each 256x256 tile will be scaled independently.
            based on the min and max values of its data.
        colormap: str, default None
            The name of the colormap to apply to the `Image`. Only valid if the `Image` has a single band.
        checkerboard: bool, default True
            Whether to display a checkerboarded background for missing or masked data.
        map: `.Map` or `.MapApp`, optional, default None
            The `.Map` (or plain ipyleaflet Map) instance on which to show the `Image`.
            If None (default), uses `wf.map <.interactive.map>`, the singleton Workflows `.MapApp` object.
        **parameters: JSON-serializable value, Proxytype, or ipywidgets.Widget
            Runtime parameters to use when computing tiles.
            Values can be any JSON-serializable value, a `Proxytype` instance, or an ipywidgets ``Widget``.

            Once these initial parameter values are set, they can be modified by assigning to
            `~.WorkflowsLayer.parameters` on the returned `WorkflowsLayer`.

            If a Widget is given, it's automatically linked, so updating the widget causes the parameter
            value to change, and the map to update. Running `visualize` again and passing in a different
            widget instance will un-link the old one automatically.

            If a Python value or `Proxytype` is given, values you later assign to that parameter
            must be of a compatible type (for example, you can't give ``threshold=0.6``, then assign
            ``lyr.parameters.threshold = "foo"``, because ``"foo"`` can't be cast to a float).

            For more information, see the docstring to `ParameterSet`.

        Returns
        -------
        layer: WorkflowsLayer
            The layer displaying this `Image`. Either a new `WorkflowsLayer` if one was created,
            or the layer with the same ``name`` that was already on the map.

        Example
        -------
        >>> import descarteslabs.workflows as wf
        >>> col = wf.ImageCollection.from_id("landsat:LC08:01:RT:TOAR")
        >>> nir, red = col.unpack_bands(["nir", "red"])
        >>> ndvi = wf.normalized_difference(nir, red)
        >>> max_ndvi = ndvi.max()
        >>> highest_ndvi = max_ndvi > wf.parameter("threshold", wf.Float)
        >>> lyr = highest_ndvi.visualize(
        ...     name="My Cool Max NDVI",
        ...     scales=[0, 1],
        ...     colormap="viridis",
        ...     threshold=0.4,
        ... )  # doctest: +SKIP
        >>> wf.map  # doctest: +SKIP
        >>> # `wf.map` actually displays the map; right click and open in new view in JupyterLab
        >>> lyr.parameters.threshold = 0.3  # doctest: +SKIP
        >>> # update map with a new value for the "threshold" parameter
        """
        from ... import interactive

        if map is None:
            map = interactive.map

        for layer in map.layers:
            if layer.name == name:
                with layer.hold_trait_notifications():
                    layer.image = self
                    layer.set_scales(scales, new_colormap=colormap)
                    layer.checkerboard = checkerboard
                    layer.set_parameters(**parameters)
                return layer
        else:
            layer = self.tile_layer(
                name=name, scales=scales, colormap=colormap, checkerboard=checkerboard, **parameters
            )
            map.add_layer(layer)
            return layer


def _result_type(other):
    ImageCollection = _DelayedImageCollection()
    return ImageCollection if isinstance(other, ImageCollection) else Image
