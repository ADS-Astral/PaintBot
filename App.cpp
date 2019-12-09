/**
 * @copyright Copyright (C) Janco Enterprise 2019. All rights reserved.
 * @license Proprietary and confidential. Unauthorized copying of this file is strictly prohibited.
 */

#include "App.h"
#include "Frame.h"

wxIMPLEMENT_APP(PaintBotApp);

bool PaintBotApp::OnInit() {

	auto frame = new PaintBotFrame("Paint Bot", wxPoint(50, 50), wxSize(450, 340));
	frame->Show(true);
	return true;
}
