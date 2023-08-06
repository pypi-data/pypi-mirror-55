** Next release **

## [v0.3.0](https://github.com/higlass/higlass-python/compare/v0.2.1...v0.3.0)

- Support multiple overlays and allow to set the `uid` and `type` options manually
- Add support for value locks via the new `value_scale_syncs` argument of `display()` and `ViewConf`
- Allow not starting FUSE by passing `no_fuse=True` to `display()`
- Update the HiGlass JavaScript library to `v1.7`

## [v0.2.1](https://github.com/higlass/higlass-python/compare/v0.2.0...v0.2.1)

- Fixed #30: Example working again
- Fixed `overlay` property by making it a property of `Views`. Also updated HiGlass to v1.6.11 to properly render overlays.

## [v0.2.0](https://github.com/higlass/higlass-python/compare/v0.1.13...v0.2.0)

- Implement two-way data bindings via traitlets. See [notebooks/two-way-data-binding.ipynb](notebooks/two-way-data-binding.ipynb) for an example
- Add `overlays` to `display` and `ViewConf` to be able to define overlays
- Store HiGlass' JavaScript API on the widget's root container. This container can be found via a random ID that is stored in `widget.dom_element_id`

## [v0.1.14](https://github.com/higlass/higlass-python/compare/v0.1.13...v0.1.14)

- Add compatibility with JupyterLab `v1` and ipywidgets `v7.5`
- Bumped HiGlass to `v1.6`

## [v0.1.13](https://github.com/higlass/higlass-python/compare/v0.1.12...v0.1.13)

- Added top-level exports of `view`, `display`, `Tileset`, `Server`, `Track`, `CombinedTrack`, `View`, and `ViewConf`

## [v0.1.12](https://github.com/higlass/higlass-python/compare/v0.1.11...v0.1.12)

- Expose dark mode in `higlass.display(dark_mode=True)`
- Do not mutate track objects in `higlass.display()` for reusability
- Further API cleaning. `ViewConf.views` is a list of views now

## [v0.1.11](https://github.com/higlass/higlass-python/compare/v0.1.10...v0.1.11)

- Convenience function for loading 2d labeled points from a dataframe.
- Remove Flask-related debugging and uninformative logs
- Add `__repr__` to `ViewConf` for convenience

## [v0.1.10](https://github.com/higlass/higlass-python/compare/v0.1.8...v0.1.10)

- Synchronized Python and node package versions

## [v0.1.8](https://github.com/higlass/higlass-python/compare/v0.1.7...v0.1.8)

- Fix installation

## [v0.1.7](https://github.com/higlass/higlass-python/compare/v0.1.1...v0.1.7)

- Bumped higlass version to `v1.5`
- Added CombinedTrack
- Added change_atributes and change_options functions

## [v0.1.1](https://github.com/higlass/higlass-python/releases/tag/v0.1.1)

- First release
