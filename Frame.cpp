/**
 * @copyright Copyright (C) Janco Enterprise 2019. All rights reserved.
 * @license Proprietary and confidential. Unauthorized copying of this file is strictly prohibited.
 */

#include "Frame.h"
#include "HashMap.h"

PaintBotFrame::PaintBotFrame(const wxString& title, const wxPoint& pos, const wxSize& size) :
	wxFrame(nullptr, wxID_ANY, title, pos, size) {

	std::string msg = std::string("GOOD");
	rs2::pipeline pipe;
	rs2::config cfg;
	rs2::frameset frames;
	rs2::frame depthframe;
	cfg.enable_stream(RS2_STREAM_DEPTH, 640, 480, RS2_FORMAT_Z16, 60);
	rs2::pipeline_profile profile;
	try {
		profile = pipe.start(cfg);
	}
	catch (rs2::error er) {
		msg = er.get_failed_args();
	}
	auto device = profile.get_device();
	auto sensor = device.first<rs2::sensor>();

	std::vector<rs2::stream_profile> stream_profiles = sensor.get_stream_profiles();
	std::map<std::pair<rs2_stream, int>, int> unique_streams;
	for (auto&& sp : stream_profiles)
	{
		unique_streams[std::make_pair(sp.stream_type(), sp.stream_index())]++;
	}
	std::cout << "Sensor consists of " << unique_streams.size() << " streams: " << std::endl;
	for (size_t i = 0; i < unique_streams.size(); i++)
	{
		auto it = unique_streams.begin();
		std::advance(it, i);
		std::cout << "  - " << it->first.first << " #" << it->first.second << std::endl;
	}

	int profile_num = 0;
	for (auto stream_profile : stream_profiles) {
		auto stream_data_type = stream_profile.stream_type();
		auto stream_index = stream_profile.stream_index();
		auto stream_name = stream_profile.stream_name();
		auto unique_stream_id = stream_profile.unique_id();

		if (stream_profile.is<rs2::video_stream_profile>()) {
			rs2::video_stream_profile video_stream_profile = stream_profile.as<rs2::video_stream_profile>();

			std::cout << " (Video Stream: " << video_stream_profile.format() << " " <<
				video_stream_profile.width() << "x" << video_stream_profile.height() << "@ " << video_stream_profile.fps() << "Hz)";
		}
		std::cout << std::endl;
		profile_num++;
	}
	int selected_profile_index = 72;
	const rs2::stream_profile& stream = stream_profiles[selected_profile_index];

	if (auto video_stream = stream.as<rs2::video_stream_profile>()) {
		rs2_intrinsics intrinsics = video_stream.get_intrinsics();
		principal_point = std::make_pair(intrinsics.ppx, intrinsics.ppy);

		PointsMap points;
		points[1] = new p3d(intrinsics.ppx, intrinsics.ppy);
	}

	/*
	sensor.set_option(RS2_OPTION_VISUAL_PRESET, RS2_RS400_VISUAL_PRESET_HIGH_ACCURACY);
	frames = pipe.wait_for_frames();
	depthframe = frames.get_depth_frame();
	auto w = 640;
	auto h = 480;
	auto pixels = (uint16_t*)depthframe.get_data();
	for (int y = 0; y < h; ++y) {
		for (int x = 0; x < w; ++x) {
			auto p = pixels[y * w + x];
		}
	}

	auto box = wxBoxSizer();
	_bmp = new wxStaticBitmap(sz_section_packages->GetStaticBox(), wxID_ANY, wxNullBitmap, wxDefaultPosition, wxSize(150, 150), 0);
	_bmp->SetBackgroundColour(wxSystemSettings::GetColour(wxSYS_COLOUR_CAPTIONTEXT));
	_bmp->SetMinSize(wxSize(150, 150));
	_bmp->SetMaxSize(wxSize(150, 150));
	sz_sizer_bmp->Add(_bmp, 0, wxALL, 5);
	*/

	wxMenu *menuFile = new wxMenu;
	menuFile->Append(ID_Hello, "&Hello...\tCtrl-H",
		"Help string shown in status bar for this menu item");
	menuFile->AppendSeparator();
	menuFile->Append(wxID_EXIT);
	wxMenu *menuHelp = new wxMenu;
	menuHelp->Append(wxID_ABOUT);
	wxMenuBar *menuBar = new wxMenuBar;
	menuBar->Append(menuFile, "&File");
	menuBar->Append(menuHelp, "&Help");
	SetMenuBar(menuBar);
	CreateStatusBar();
	//SetStatusText(msg.c_str());
}

void PaintBotFrame::OnExit(wxCommandEvent& event) {

	Close(true);
}

void PaintBotFrame::OnAbout(wxCommandEvent& event) {

	SetStatusText(std::to_string(principal_point.first) + ", " + std::to_string(principal_point.second));
}

void PaintBotFrame::OnHello(wxCommandEvent& event) {

	wxLogMessage("Hello world from wxWidgets!");
}
