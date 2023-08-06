from bbrc.validation.test import Results

def aget_cmap():
    import bbrc
    import numpy as np
    import os.path as op

    fn = 'FreeSurferColorLUT.txt'
    fp = op.join(op.dirname(bbrc.__file__), 'data', fn)
    data = open(fp).read().split('\n')
    lut = [[each for each in e.split(' ') if each != ''] \
           for e in data if not e.startswith('#') and len(e) != 0]
    LUT = {each[0]: [int(e) for e in each[2:5]] for each in lut}
    LUT = [LUT.get(str(i), [255, 255, 255]) for i in range(0, 2035)]
    LUT = np.array(LUT)
    LUT = LUT / 255.0
    return LUT


def probamap_snapshot(t1_fp, c1_fp):
    from nilearn import plotting
    import tempfile

    paths = []
    for each in 'xyz':
        _, path = tempfile.mkstemp(suffix='.jpg')
        paths.append(path)
        im = plotting.plot_anat(t1_fp, draw_cross=False, display_mode=each, cut_coords=10)
        im.add_overlay(c1_fp)
        im.savefig(path)
    return paths


def topup_snapshot(pre_fp, post_fp):
    from nilearn import plotting, image
    import tempfile

    # compute a threshold for the overlay based on range of intensity values
    data = image.load_img(post_fp).get_fdata()
    val_range = abs(data.min()) + abs(data.max())
    thresh = val_range / 6

    paths = []
    for each in 'xyz':
        _, path = tempfile.mkstemp(suffix='.jpg')
        paths.append(path)
        im = plotting.plot_anat(pre_fp,
                                black_bg=True,
                                bg_img=None,
                                display_mode=each,
                                draw_cross=False,
                                cmap='black_green')
        im.add_overlay(post_fp,
                       threshold=thresh,
                       cmap='black_red')
        im.savefig(path)
    return paths


def snapshot(image1_mri_path, image2_mri_path, mode='ANTS'):
    import logging as log
    from matplotlib.colors import ListedColormap
    from visualqc import config as cfg
    import matplotlib as mpl
    mpl.use('Agg')
    from matplotlib import cm, colors, pyplot as plt
    import numpy as np
    from visualqc.utils import get_axis, pick_slices, read_image, scale_0to1
    from mrivis.utils import crop_to_seg_extents
    import tempfile
    if mode == 'ANTS':
        from visualqc.image_utils import overlay_edges, mix_color, diff_image, mix_slices_in_checkers
    import os

    if mode == 'FreeSurfer':
        LUT = aget_cmap()
        cmap = ListedColormap(LUT)

    views = [0, 1, 2]
    num_slices_per_view = cfg.default_num_slices
    num_rows_per_view = cfg.default_num_rows
    alpha_mri = 1.0
    alpha_seg = 0.7
    normalize_mri = colors.Normalize(vmin=0, vmax=1, clip=True)
    mri_mapper = cm.ScalarMappable(norm=normalize_mri, cmap='gray')


    empty_image = np.full((10, 10, 3), 0.0)
    display_params = dict(interpolation='none', aspect='equal',
                              origin='lower',
                              alpha=alpha_mri)
    padding = cfg.default_padding
    num_cols_volumetric = num_slices_per_view / num_rows_per_view
    num_rows_total = len(views) * num_rows_per_view
    total_num_panels = int(num_cols_volumetric * num_rows_total)

    image_one = read_image(image1_mri_path, error_msg='T1 mri')
    image_two = read_image(image2_mri_path, error_msg='T2 mri')


    if mode == 'FreeSurfer':
        image_one2 = scale_0to1(image_one, cfg.max_cmap_range_t1_mri)
        image_two2 = image_two
    elif mode == 'ANTS':
        image_one2 = scale_0to1(image_one)
        image_two2 = scale_0to1(image_two)

    image_one1, image_two1 = crop_to_seg_extents(image_one2, image_two2, padding)


    if mode == 'FreeSurfer':
        num_labels = len(cmap.colors)
        label_set = cfg.default_label_set
        unique_labels = np.arange(num_labels, dtype='int16')

        normalize_labels = colors.Normalize(vmin=0, vmax=num_labels, clip=True)
        seg_mapper = cm.ScalarMappable(norm=normalize_labels, cmap=cmap)
        unique_labels_display = np.setdiff1d(unique_labels, 0)
        color_for_label = seg_mapper.to_rgba(unique_labels_display)

        def plot_contours_in_slice(slice_seg, target_axis):
            """Plots contour around the data in slice (after binarization)"""

            plt.sca(target_axis)
            contour_handles = list()

            for index, label in enumerate(unique_labels_display):
                binary_slice_seg = slice_seg == index
                if not binary_slice_seg.any():
                    continue
                ctr_h = plt.contour(binary_slice_seg,
                                    levels=[cfg.contour_level, ],
                                    colors=(color_for_label[index],),
                                    linewidths=cfg.contour_line_width,
                                    alpha=alpha_seg,
                                    zorder=cfg.seg_zorder_freesurfer)
                contour_handles.append(ctr_h)

            return contour_handles


        slices = pick_slices(image_two1, views, num_slices_per_view)

    elif mode == 'ANTS':
        slices = pick_slices(image_one1, views, num_slices_per_view)

    num_cols_final = int(np.ceil(total_num_panels / num_rows_total))

    figsize = cfg.default_review_figsize
    plt.style.use('dark_background')
    fig, axes = plt.subplots(num_rows_total, num_cols_final,
                                       figsize=(30,20))
    axes = axes.flatten()

    num_volumetric_panels = len(axes)
    h_images = [None] * num_volumetric_panels
    if mode == 'ANTS':
        h_slice_numbers = [None] * len(axes)
        empty_image = np.full((100, 100, 3), 0.0)
        label_x, label_y = 5, 5 # in image space

    for ix, ax in enumerate(axes[0:]):
        ax.axis('off')
        h_images[ix] = ax.imshow(empty_image, **display_params)
        if mode == 'ANTS':
            h_slice_numbers[ix]= ax.text(label_x, label_y, '',
                              **cfg.slice_num_label_properties)

    if mode == 'FreeSurfer':
        for vol_ax_index, (dim_index, slice_index) in enumerate(slices):
            print(vol_ax_index)
            panel_index = vol_ax_index
            plt.sca(axes[panel_index])
            slice_mri = get_axis(image_one1, dim_index, slice_index)
            slice_seg = get_axis(image_two1, dim_index, slice_index)

            mri_rgba = mri_mapper.to_rgba(slice_mri, alpha=alpha_mri)
            h_m = plt.imshow(mri_rgba, interpolation='none',
                             aspect='equal', origin='lower')
            h_seg = plot_contours_in_slice(slice_seg, axes[panel_index])

    elif mode == 'ANTS':
        from functools import partial
        mixer = partial(overlay_edges, sharper=False)

        for ax_index, (dim_index, slice_index) in enumerate(slices):
            slice_one = get_axis(image_one1, dim_index, slice_index)
            slice_two = get_axis(image_two1, dim_index, slice_index)
            mixed_slice = mixer(slice_one, slice_two)
            # mixed_slice is already in RGB mode m x p x 3, so
            #   prev. cmap (gray) has no effect on color_mixed data
            h_images[ax_index].set(data=mixed_slice, cmap=None)
            h_slice_numbers[ax_index].set_text(str(slice_index))

    fd, snap_fp = tempfile.mkstemp(suffix='.jpg')
    plt.savefig(snap_fp)
    os.close(fd)
    return Results(True, data=[snap_fp])
