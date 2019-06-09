def json(city):
    return {
        "version": "v1",
        "config": {
            "visState": {
                "filters": [
                    {
                        "dataId": "barangays",
                        "id": "barangays_filter",
                        "name": "desirability",
                        "type": "range",
                        "value": [
                            0,
                            100
                        ],
                        "enlarged": False,
                        "plotType": "histogram",
                        "yAxis": None
                    },
                    {
                        "dataId": "amenities",
                        "id": "amenities_filter",
                        "name": "class",
                        "type": "multiSelect",
                        # "value": city.amenity_types(),
                        "value": [],
                        "enlarged": False,
                        "plotType": "histogram",
                        "yAxis": None
                    },
                    {
                        "dataId": "pairs",
                        "id": "pairs_filter",
                        "name": "o_id",
                        "type": "range",
                        "value": [
                            0,
                            0
                        ],
                        "enlarged": False,
                        "plotType": "histogram",
                        "yAxis": None
                    }
                ],
                "layers": [
                    {
                        "id": "pairs_layer",
                        "type": "arc",
                        "config": {
                            "dataId": "pairs",
                            "label": "Pairs",
                            "color": [
                                38,
                                26,
                                16
                            ],
                            "columns": {
                                "lat0": "o_lat",
                                "lng0": "o_long",
                                "lat1": "d_lat",
                                "lng1": "d_long"
                            },
                            "isVisible": True,
                            "visConfig": {
                                "opacity": 0.6,
                                "thickness": 8,
                                "colorRange": {
                                    "name": "Uber Viz Sequential 4",
                                    "type": "sequential",
                                    "category": "Uber",
                                    "colors": [
                                        "#E6FAFA",
                                        "#C1E5E6",
                                        "#9DD0D4",
                                        "#75BBC1",
                                        "#4BA7AF",
                                        "#00939C"
                                    ],
                                    "reversed": False
                                },
                                "sizeRange": [
                                    0,
                                    10
                                ],
                                "targetColor": [
                                    136,
                                    106,
                                    83
                                ],
                                "hi-precision": False
                            },
                            "textLabel": {
                                "field": None,
                                "color": [
                                    255,
                                    255,
                                    255
                                ],
                                "size": 50,
                                "offset": [
                                    0,
                                    0
                                ],
                                "anchor": "middle"
                            }
                        },
                        "visualChannels": {
                            "colorField": {
                                "name": "count",
                                "type": "integer"
                            },
                            "colorScale": "quantile",
                            "sizeField": None,
                            "sizeScale": "linear"
                        }
                    },
                    {
                        "id": "amenities_layer",
                        "type": "icon",
                        "config": {
                            "dataId": "amenities",
                            "label": "Amenity",
                            "color": [
                                248,
                                248,
                                255
                            ],
                            "columns": {
                                "lat": "latitude",
                                "lng": "longitude",
                                "icon": "icon"
                            },
                            "isVisible": True,
                            "visConfig": {
                                "radius": 35,
                                "fixedRadius": False,
                                "opacity": 0.6,
                                "colorRange": {
                                    "name": "Uber Viz Qualitative 4",
                                    "type": "qualitative",
                                    "category": "Uber",
                                    "colors": city.amenity_colors(),
                                    "reversed": False
                                },
                                "radiusRange": [
                                    0,
                                    50
                                ],
                                "hi-precision": False
                            },
                            "textLabel": {
                                "field": None,
                                "color": [
                                    255,
                                    255,
                                    255
                                ],
                                "size": 50,
                                "offset": [
                                    0,
                                    0
                                ],
                                "anchor": "middle"
                            }
                        },
                        "visualChannels": {
                            # "colorField": {
                            #     "name": "class",
                            #     "type": "string"
                            # },
                            "colorField": None,
                            "colorScale": "ordinal",
                            "sizeField": None,
                            "sizeScale": "linear"
                        }
                    },
                    {
                        "id": "center_layer",
                        "type": "point",
                        "config": {
                            "dataId": "barangays",
                            "label": "Center",
                            "color": [
                                23,
                                184,
                                190
                            ],
                            "columns": {
                                "lat": "latitude",
                                "lng": "longitude",
                                "altitude": None
                            },
                            "isVisible": False,
                            "visConfig": {
                                "radius": 10,
                                "fixedRadius": False,
                                "opacity": 0.8,
                                "outline": False,
                                "thickness": 2,
                                "colorRange": {
                                    "name": "Global Warming",
                                    "type": "sequential",
                                    "category": "Uber",
                                    "colors": [
                                        "#5A1846",
                                        "#900C3F",
                                        "#C70039",
                                        "#E3611C",
                                        "#F1920E",
                                        "#FFC300"
                                    ]
                                },
                                "radiusRange": [
                                    0,
                                    50
                                ],
                                "hi-precision": False
                            },
                            "textLabel": {
                                "field": None,
                                "color": [
                                    255,
                                    255,
                                    255
                                ],
                                "size": 50,
                                "offset": [
                                    0,
                                    0
                                ],
                                "anchor": "middle"
                            }
                        },
                        "visualChannels": {
                            "colorField": None,
                            "colorScale": "quantile",
                            "sizeField": None,
                            "sizeScale": "linear"
                        }
                    },
                    {
                        "id": "barangays_layer",
                        "type": "geojson",
                        "config": {
                            "dataId": "barangays",
                            "label": "Barangay",
                            "color": [
                                246,
                                209,
                                138,
                                255
                            ],
                            "columns": {
                                "geojson": "_geojson"
                            },
                            "isVisible": True,
                            "visConfig": {
                                "opacity": 0.8,
                                "thickness": 0.5,
                                "colorRange": {
                                    "name": "ColorBrewer YlOrRd-6",
                                    "type": "sequential",
                                    "category": "ColorBrewer",
                                    "colors": [
                                        "#bd0026",
                                        "#f03b20",
                                        "#fd8d3c",
                                        "#feb24c",
                                        "#fed976",
                                        "#ffffb2"
                                    ],
                                    "reversed": True
                                },
                                "radius": 10,
                                "sizeRange": [
                                    0,
                                    10
                                ],
                                "radiusRange": [
                                    0,
                                    50
                                ],
                                "heightRange": [
                                    0,
                                    500
                                ],
                                "elevationScale": 5,
                                "hi-precision": False,
                                "stroked": True,
                                "filled": True,
                                "enable3d": False,
                                "wireframe": False
                            },
                            "textLabel": {
                                "field": None,
                                "color": [
                                    255,
                                    255,
                                    255
                                ],
                                "size": 50,
                                "offset": [
                                    0,
                                    0
                                ],
                                "anchor": "middle"
                            }
                        },
                        "visualChannels": {
                            "colorField": {
                                "name": "desirability",
                                "type": "real"
                            },
                            "colorScale": "quantile",
                            "sizeField": None,
                            "sizeScale": "linear",
                            "heightField": None,
                            "heightScale": "linear",
                            "radiusField": None,
                            "radiusScale": "linear"
                        }
                    },
                    {
                        "id": "outline_layer",
                        "type": "geojson",
                        "config": {
                            "dataId": "outline",
                            "label": "Barangay outline",
                            "color": [
                                128, 128, 128
                            ],
                            "columns": {
                                "geojson": "_geojson"
                            },
                            "isVisible": True,
                            "visConfig": {
                                "opacity": 0.05,
                                "thickness": 0.5,
                                "colorRange": {
                                    "name": "Global Warming",
                                    "type": "sequential",
                                    "category": "Uber",
                                    "colors": [
                                        "#5A1846",
                                        "#900C3F",
                                        "#C70039",
                                        "#E3611C",
                                        "#F1920E",
                                        "#FFC300"
                                    ]
                                },
                                "radius": 10,
                                "sizeRange": [
                                    0,
                                    10
                                ],
                                "radiusRange": [
                                    0,
                                    50
                                ],
                                "heightRange": [
                                    0,
                                    500
                                ],
                                "elevationScale": 5,
                                "hi-precision": False,
                                "stroked": True,
                                "filled": True,
                                "enable3d": False,
                                "wireframe": False
                            },
                            "textLabel": {
                                "field": None,
                                "color": [
                                    255,
                                    255,
                                    255
                                ],
                                "size": 50,
                                "offset": [
                                    0,
                                    0
                                ],
                                "anchor": "middle"
                            }
                        },
                        "visualChannels": {
                            "colorField": None,
                            "colorScale": "quantile",
                            "sizeField": None,
                            "sizeScale": "linear",
                            "heightField": None,
                            "heightScale": "linear",
                            "radiusField": None,
                            "radiusScale": "linear"
                        }
                    }
                ],
                "interactionConfig": {
                    "tooltip": {
                        "fieldsToShow": {
                            "barangays": [
                                "name",
                                "desirability"
                            ],
                            "amenities": [
                                "name",
                                "barangay",
                                "class",
                                "type"
                            ],
                            "outline": [],
                            "pairs": [
                                "count"
                            ]
                        },
                        "enabled": True
                    },
                    "brush": {
                        "size": 0.5,
                        "enabled": False
                    }
                },
                "layerBlending": "normal",
                "splitMaps": []
            }
        }
    }
