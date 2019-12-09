/**
 * @copyright Copyright (C) Janco Enterprise 2019. All rights reserved.
 * @license Proprietary and confidential. Unauthorized copying of this file is strictly prohibited.
 */

#pragma once

#include <wx/wxprec.h>
#ifndef WX_PRECOMP
#include <wx/wx.h>
#endif

struct p3d {

	float x, y, z;

	p3d(float _x, float _y, float _z = 0) : x(_x), y(_y), z(_z) {}
};

WX_DECLARE_HASH_MAP(int, p3d*, wxIntegerHash, wxIntegerEqual, PointsMap);
