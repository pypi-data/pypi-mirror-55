# -*- coding: utf-8 -*-
from pyramid.tweens import EXCVIEW


def includeme(config):  # pragma: no cover
    """
    :type config: :class:`pyramid.config.Configurator`
    """
    config.add_tween('pyramid_zipkin.tween.zipkin_tween', over=EXCVIEW)
