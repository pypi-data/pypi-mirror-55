import datetime
import uuid
import threading

import ipyleaflet
import ipywidgets as widgets
import traitlets


from ..models import XYZ
from ..types import Image

from . import parameters
from .clearable import ClearableOutput


class ScaleFloat(traitlets.CFloat):
    "Casting Float traitlet that also considers the empty string as None"

    def validate(self, obj, value):
        if value == "" and self.allow_none:
            return None
        return super(ScaleFloat, self).validate(obj, value)


class WorkflowsLayer(ipyleaflet.TileLayer):
    """
    Subclass of ``ipyleaflet.TileLayer`` for displaying a Workflows `~.geospatial.Image`.

    Attributes
    ----------
    image: ~.geospatial.Image
        The `~.geospatial.Image` to use
    parameters: ParameterSet
        Parameters to use while computing; modify attributes under ``.parameters``
        (like ``layer.parameters.foo = "bar"``) to cause the layer to recompute
        and update under those new parameters.
    xyz_obj: ~.models.XYZ
        Read-only: The `XYZ` object this layer is displaying.
    session_id: str
        Read-only: Unique ID that error logs will be stored under, generated automatically.
    checkerboard: bool, default True
        Whether to display a checkerboarded background for missing or masked data.
    colormap: str, optional, default None
        Name of the colormap to use.
        If set, `image` must have 1 band.
    cmap_min: float, optional, default None
        Min value for scaling the single band when a `colormap` is given.
    cmap_max: float, optional, default None
        Max value for scaling the single band when a `colormap` is given.
    r_min: float, optional, default None
        Min value for scaling the red band.
    r_max: float, optional, default None
        Max value for scaling the red band.
    g_min: float, optional, default None
        Min value for scaling the green band.
    g_max: float, optional, default None
        Max value for scaling the green band.
    b_min: float, optional, default None
        Min value for scaling the blue band.
    b_max: float, optional, default None
        Max value for scaling the blue band.
    error_output: ipywidgets.Output, optional, default None
        If set, write unique errors from tiles computation to this output area
        from a background thread. Setting to None stops the listener thread.
    """

    attribution = traitlets.Unicode("Descartes Labs").tag(sync=True, o=True)
    min_zoom = traitlets.Int(5).tag(sync=True, o=True)
    url = traitlets.Unicode(read_only=True).tag(sync=True)

    image = traitlets.Instance(Image)
    parameters = traitlets.Instance(parameters.ParameterSet, allow_none=True)
    xyz_obj = traitlets.Instance(XYZ, read_only=True)
    session_id = traitlets.Unicode(read_only=True)

    checkerboard = traitlets.Bool(True)
    colormap = traitlets.Unicode(None, allow_none=True)
    cmap_min = ScaleFloat(None, allow_none=True)
    cmap_max = ScaleFloat(None, allow_none=True)

    r_min = ScaleFloat(None, allow_none=True)
    r_max = ScaleFloat(None, allow_none=True)
    g_min = ScaleFloat(None, allow_none=True)
    g_max = ScaleFloat(None, allow_none=True)
    b_min = ScaleFloat(None, allow_none=True)
    b_max = ScaleFloat(None, allow_none=True)

    error_output = traitlets.Instance(widgets.Output, allow_none=True)
    autoscale_progress = traitlets.Instance(ClearableOutput)

    def __init__(self, image, *args, **kwargs):
        params = kwargs.pop("parameters", {})
        super(WorkflowsLayer, self).__init__(*args, **kwargs)

        with self.hold_trait_notifications():
            self.image = image
            self.set_trait("session_id", uuid.uuid4().hex)
            self.set_trait("autoscale_progress", ClearableOutput(widgets.Output()))
            self.set_parameters(**params)

        self._error_listener = None
        self._known_errors = set()
        self._known_errors_lock = threading.Lock()

    def make_url(self):
        """
        Generate the URL for this layer.

        This is called automatically as the attributes (`image`, `colormap`, scales, etc.) are changed.
        """
        if not self.visible:
            # workaround for the fact that Leaflet still loads tiles from inactive layers,
            # which is expensive computation users don't want
            return ""

        if self.colormap is not None:
            scales = [[self.cmap_min, self.cmap_max]]
        else:
            scales = [
                [self.r_min, self.r_max],
                [self.g_min, self.g_max],
                [self.b_min, self.b_max],
            ]

        scales = [scale for scale in scales if scale != [None, None]]

        parameters = self.parameters.to_dict()

        return self.xyz_obj.url(
            session_id=self.session_id,
            colormap=self.colormap,
            scales=scales,
            checkerboard=self.checkerboard,
            **parameters
        )

    @traitlets.observe("image")
    def _update_xyz(self, change):
        old, new = change["old"], change["new"]
        if old is new:
            # traitlets does an == check between the old and new value to decide if it's changed,
            # which for an Image, returns another Image, which it considers changed.
            return

        xyz = XYZ.build(new, name=self.name)
        xyz.save()
        self.set_trait("xyz_obj", xyz)

    @traitlets.observe(
        "visible",
        "checkerboard",
        "colormap",
        "r_min",
        "r_max",
        "g_min",
        "g_max",
        "b_min",
        "b_max",
        "cmap_min",
        "cmap_max",
        "xyz_obj",
        "session_id",
        "parameters",
    )
    @traitlets.observe("parameters", type="delete")
    def _update_url(self, change):
        self.set_trait("url", self.make_url())

    @traitlets.observe("parameters", type="delete")
    def _update_url_on_param_delete(self, change):
        # traitlets is dumb and decorator stacking doesn't work so we have to repeat this
        self.set_trait("url", self.make_url())

    @traitlets.observe("xyz_obj", "session_id")
    def _update_error_logger(self, change):
        if self.error_output is None:
            return

        if self._error_listener is not None:
            self._error_listener.stop(timeout=1)

        listener = self.xyz_obj.error_listener()
        listener.add_callback(self._log_errors_callback)
        listener.listen(self.session_id, datetime.datetime.now())

        self._error_listener = listener

    def _stop_error_logger(self):
        if self._error_listener is not None:
            self._error_listener.stop(timeout=1)
            self._error_listener = None

    @traitlets.observe("error_output")
    def _toggle_error_listener_if_output(self, change):
        if change["new"] is None:
            self._stop_error_logger()
        else:
            if self._error_listener is None:
                self._update_error_logger({})

    def _log_errors_callback(self, msg):
        message = msg.message

        with self._known_errors_lock:
            if message in self._known_errors:
                return
            else:
                self._known_errors.add(message)

        error = "{}: {}\n".format(self.name, message)
        self.error_output.append_stdout(error)

    def __del__(self):
        self._stop_error_logger()
        super(WorkflowsLayer, self).__del__()

    def forget_errors(self):
        "Clear the set of known errors, so they are re-displayed if they occur again"
        with self._known_errors_lock:
            self._known_errors.clear()

    def set_scales(self, scales, new_colormap=False):
        """
        Update the scales for this layer by giving a list of scales

        Parameters
        ----------
        scales: list of lists, default None
            The scaling to apply to each band in the `Image`.

            If `Image` contains 3 bands, ``scales`` must be a list like ``[(0, 1), (0, 1), (-1, 1)]``.

            If `Image` contains 1 band, ``scales`` must be a list like ``[(0, 1)]``,
            or just ``(0, 1)`` for convenience

            If None, each 256x256 tile will be scaled independently
            based on the min and max values of its data.
        new_colormap: str, None, or False, optional, default False
            A new colormap to set at the same time, or False to use the current colormap.
        """
        colormap = self.colormap if new_colormap is False else new_colormap

        if scales is not None:
            scales = XYZ._validate_scales(scales)

            scales_len = 1 if colormap is not None else 3
            if len(scales) != scales_len:
                msg = "Expected {} scales, but got {}.".format(scales_len, len(scales))
                if len(scales) in (1, 2):
                    msg += " If displaying a 1-band Image, use a colormap."
                elif colormap:
                    msg += " Colormaps cannot be used with multi-band images."

                raise ValueError(msg)

            with self.hold_trait_notifications():
                if colormap is None:
                    self.r_min = scales[0][0]
                    self.r_max = scales[0][1]
                    self.g_min = scales[1][0]
                    self.g_max = scales[1][1]
                    self.b_min = scales[2][0]
                    self.b_max = scales[2][1]
                else:
                    self.cmap_min = scales[0][0]
                    self.cmap_max = scales[0][1]
                if new_colormap is not False:
                    self.colormap = new_colormap
        else:
            # scales is None
            with self.hold_trait_notifications():
                if colormap is None:
                    self.r_min = None
                    self.r_max = None
                    self.g_min = None
                    self.g_max = None
                    self.b_min = None
                    self.b_max = None
                else:
                    self.cmap_min = None
                    self.cmap_max = None
                if new_colormap is not False:
                    self.colormap = new_colormap

    def set_parameters(self, **params):
        """
        Set new parameters for this `WorkflowsLayer`.

        In typical cases, you update parameters by assigning to `parameters`
        (like ``layer.parameters.threshold = 6.6``).

        Instead, use this function when you need to change the *names or types*
        of parameters available on the `WorkflowsLayer`. (Users shouldn't need to
        do this, as `~.Image.visualize` handles it for you, but custom widget developers
        may need to use this method when they change the `image` field on a `WorkflowsLayer`.)

        If a value is an ipywidgets Widget, it will be linked to that parameter
        (via its ``"value"`` attribute). If a parameter was previously set with
        a widget, and a different widget instance (or non-widget) is passed
        for its new value, the old widget is automatically unlinked.
        If the same widget instance is passed as is already linked, no change occurs.

        Parameters
        ----------
        params: JSON-serializable value, Proxytype, or ipywidgets.Widget
            Paramter names to new values. Values can be Python types,
            `Proxytype` instances, or ``ipywidgets.Widget`` instances.
        """
        param_set = self.parameters
        if param_set is None:
            param_set = self.parameters = parameters.ParameterSet(self, "parameters")

        with self.hold_trait_notifications():
            param_set.update(**params)

    def _ipython_display_(self):
        param_set = self.parameters
        if param_set:
            widget = param_set.widget
            if widget and len(widget.children) > 0:
                widget._ipython_display_()
