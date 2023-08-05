//showcase
PyDoc_STRVAR(texture_doc,
	"Textures are RGBA bitmap image objects \n"\
	"\n"\
	"tex = pyxie.texture()");

//setImage
PyDoc_STRVAR(setImage_doc,
	"Set byte image to texture object\n"\
	"\n"\
	"texture.setImage(image, x, y, width,height)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    image : Bytes or numpy.ndarray\n"\
	"        array of rgb or rgba image\n"\
	"    x : int (optional)\n"\
	"        x offset of destination\n"\
	"    y : int (optional)\n"\
	"        y offset of destination\n"\
	"    width : int (optional)\n"\
	"        copy image width\n"\
	"    height : int (optional)\n"\
	"        copy image height\n");


//setCheckeredImage
PyDoc_STRVAR(setCheckeredImage_doc,
	"Set checkerd image to texture object\n"\
	"\n"\
	"texture.setCheckeredImage(r, g, b)\n"\
	"\n"\
	"Parameters\n"\
	"----------\n"\
	"    r,g,b : int (optional)\n"\
	"        checker color (0 - 255)\n"\
	"        default color is green");
