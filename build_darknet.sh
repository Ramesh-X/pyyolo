#!/usr/bin/env bash

# arguments order
# darknet_home, download_again, GPU, CUDNN, OPENCV, OPENMP

DARKNET_HOME=$1
DOWNLOAD_AGAIN=$2
HERE=`pwd -P`

command -v git >/dev/null 2>&1 || { echo >&2 "This requires git, but it's not installed.  Aborting.."; exit 1; }
command -v make >/dev/null 2>&1 || { echo >&2 "This requires make, but it's not installed.  Aborting.."; exit 1; }

mkdir -p ${DARKNET_HOME}
cd ${DARKNET_HOME}

if [ "${DOWNLOAD_AGAIN}" -eq "1" ]; then
    cd ..
    rm -rf darknet
    git clone https://github.com/pjreddie/darknet.git
    cd darknet
fi

sed -i "1s/.*/GPU=$3/" Makefile
sed -i "2s/.*/CUDNN=$4/" Makefile
sed -i "3s/.*/OPENCV=$5/" Makefile
sed -i "4s/.*/OPENMP=$6/" Makefile

if ! grep -Fxq "image ndarray_to_image(unsigned char* src, long* shape, long* strides);" ./src/image.h
then
echo "image ndarray_to_image(unsigned char* src, long* shape, long* strides)
{
    int h = shape[0];
    int w = shape[1];
    int c = shape[2];
    int step_h = strides[0];
    int step_w = strides[1];
    int step_c = strides[2];
    image im = make_image(w, h, c);
    int i, j, k;
    int index1, index2 = 0;

    for(i = 0; i < h; ++i){
            for(k= 0; k < c; ++k){
                for(j = 0; j < w; ++j){

                    index1 = k*w*h + i*w + j;
                    index2 = step_h*i + step_w*j + step_c*k;
                    //fprintf(stderr, "w=%d h=%d c=%d step_w=%d step_h=%d step_c=%d \n", w, h, c, step_w, step_h, step_c);
                    //fprintf(stderr, "im.data[%d]=%u data[%d]=%f \n", index1, src[index2], index2, src[index2]/255.);
                    im.data[index1] = src[index2]/255.;
                }
            }
        }

    rgbgr_image(im);

    return im;
}" >> ./src/image.c

sed "46iimage ndarray_to_image(unsigned char* src, long* shape, long* strides);" ./src/image.h > ./src/image.h.tmp
mv ./src/image.h.tmp ./src/image.h
fi

make -j$(nproc)
cp libdarknet.so ${HERE}/pyyolo



