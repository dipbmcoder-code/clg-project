exports.shorthands = undefined;

exports.up = (pgm) => {
    pgm.renameColumn('websites', 'social_media_categories', 'x_categories');
};

exports.down = (pgm) => {
    pgm.renameColumn('websites', 'x_categories', 'social_media_categories');
};
