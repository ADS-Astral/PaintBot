/**
 * @copyright Copyright (C) Janco Enterprise 2019. All rights reserved.
 * @license Proprietary and confidential. Unauthorized copying of this file is strictly prohibited.
 */

#pragma once

#include "App.h"

#ifdef _MSC_VER
#pragma warning(push)
#pragma warning(disable : 4996)
#endif

#include <librealsense2/rs.hpp>
#include "example.hpp"


#include <map>
#include <string>
#include <thread>
#include <atomic>

#include <imgui.h>
#include "imgui_impl_glfw.h"

class PaintBotFrame : public wxFrame {

public:

	PaintBotFrame(const wxString& title, const wxPoint& pos, const wxSize& size);

private:

	std::pair<float, float> principal_point;

	void OnHello(wxCommandEvent& event);
	void OnExit(wxCommandEvent& event);
	void OnAbout(wxCommandEvent& event);

	wxDECLARE_EVENT_TABLE();
};

enum {

	ID_Hello = wxID_HIGHEST + 1,
};

wxBEGIN_EVENT_TABLE(PaintBotFrame, wxFrame)
EVT_MENU(ID_Hello, PaintBotFrame::OnHello)
EVT_MENU(wxID_EXIT, PaintBotFrame::OnExit)
EVT_MENU(wxID_ABOUT, PaintBotFrame::OnAbout)
wxEND_EVENT_TABLE()
