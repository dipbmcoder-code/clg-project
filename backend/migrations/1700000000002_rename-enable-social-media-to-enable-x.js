exports.shorthands = undefined;

exports.up = (pgm) => {
    pgm.renameColumn('websites', 'enable_social_media', 'enable_x');
};

exports.down = (pgm) => {
    pgm.renameColumn('websites', 'enable_x', 'enable_social_media');
};
