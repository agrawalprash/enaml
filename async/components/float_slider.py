#------------------------------------------------------------------------------
#  Copyright (c) 2011, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from traits.api import Constant, Float, Property, Range, TraitError, \
    on_trait_change

from .slider import Slider, MAX_SLIDER_VALUE


class FloatSlider(Slider):
    """ A simple slider widget that can be used to select from a 
    range of floating point values.

    """
    #: The minimum value for the index. To avoid issues where
    #: :attr:`minimum` is higher than :attr:`maximum`. The value is
    #: a positive integer capped by the :attr:`maximum`. If the new
    #: value of :attr:`minimum` make the current position invalid then
    #: the current position is set to :attr:minimum. Default value is 0.0.
    minimum = Property(Float, depends_on ='_minimum')

    #: The internal minimum storage
    _minimum = Float(0)

    #: The maximum value for the index. Checks make sure that
    #: :attr:`maximum` cannot be lower than :attr:`minimum`. If the
    #: new value of :attr:`maximum` make the current position invalid
    #: then the current position is set to :attr:maximum. Default value is 1.0.
    maximum = Property(Float, depends_on ='_maximum')

    #: The internal maximum storage
    _maximum = Float(1.0)

    #: The number of integer steps allowed by the slider. Default value is 100.
    precision = Range(value=100, low=1, high=MAX_SLIDER_VALUE)

    #: The interval to put between tick marks in integer units step units.
    #: Default value is `10`.
    tick_interval = Range(low='_one', high='precision', value=10, exclude_high=True)
    _one = Constant(1)

    #: Defines the number of steps that the slider will move when the
    #: user presses the page_up/page_down keys. Default is 10.
    page_step = Range(low='_one', high='precision', value=10)

    #--------------------------------------------------------------------------
    # Toolkit Communication
    #--------------------------------------------------------------------------
    @on_trait_change('precision, maximum, minimum, tick_interval, page_step')
    def sync_object_state(self, name, new):
        """ Notify the client component of updates to the object state.

        """
        msg = 'set_' + name
        self.send(msg, {'value':new})

    def initial_attrs(self):
        """ Return a dictionary which contains all the state necessary to
        initialize a client widget.

        """
        super_attrs = super(FloatSlider, self).initial_attrs()
        attrs = {
            'maximum' : self.maximum,
            'minimum' : self.minimum,
            'precision' : self.precision,
            'tick_interval' : self.tick_interval,
            'page_step' : self.page_step
        }
        super_attrs.update(attrs)
        return super_attrs
    
    #--------------------------------------------------------------------------
    # Property methods
    #--------------------------------------------------------------------------
    def _set_minimum(self, value):
        """ The property setter for the 'minimum' attribute. This
        validates that the value is always smaller than :attr:`maximum`.
        This is an overridden parent class method.

        """
        if (value > self.maximum):
            msg = ('The minimum value of the slider should be a smaller '
                   'than the current maximum ({0}), '
                   'but a value of {1} was given')
            msg = msg.format(self.maximum, value)
            raise TraitError(msg)
        else:
            self._minimum = value

    def _set_maximum(self, value):
        """ The property setter for the 'maximum' attribute. This
        validates that the value is always larger than :attr:`minimum`.
        This is an overridden parent class method.

        """
        if (value < self.minimum):
            msg = ("The maximum value of the slider should be "
                   "larger than the current minimum ({0}), "
                   "but a value of {1} was given")
            msg = msg.format(self.minimum, value)
            raise TraitError(msg)
        else:
            self._maximum = value

    def _get_maximum(self):
        """ The property getter for the slider maximum. Even though this
        is identical to the parent class method, it is required since we
        redefine the property on this class.

        """
        return self._maximum

    def _get_minimum(self):
        """ The property getter for the slider minimum. Even though this
        is identical to the parent class method, it is required since we
        redefine the property on this class.

        """
        return self._minimum
        
