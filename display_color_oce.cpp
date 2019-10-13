//=============================================================================

//function : VColorScale

//purpose  : representation color scale

//=============================================================================

#include <V3d_ColorScale.hxx>

static int VColorScale(Draw_Interpretor &di, Standard_Integer argc, const char **argv)

{

    if (argc != 1 && argc != 4 && argc != 5 && argc != 6 && argc != 8)

    {

        di << "Usage : " << argv[0] << " [RangeMin = 0 RangeMax = 100 Intervals = 10 HeightFont = 16 Position = Right X = 0 Y = 0]  "
           << "\n";

        return 1;
    }

    Handle(AIS_InteractiveContext) aContext = ViewerTest::GetAISContext();

    if (aContext.IsNull())
    {

        di << argv[0] << " ERROR : use 'vinit' command before "
           << "\n";

        return -1;
    }

    Standard_Real minRange = 0., maxRange = 100.;

    Standard_Integer numIntervals = 10;

    Standard_Integer textHeight = 16;

    Aspect_TypeOfColorScalePosition position = Aspect_TOCSP_RIGHT;

    Standard_Real X = 0., Y = 0.;

    if (argc < 9)

    {

        if (argc > 3)

        {

            minRange = Draw::Atof(argv[1]);

            maxRange = Draw::Atof(argv[2]);

            numIntervals = Draw::Atoi(argv[3]);
        }

        if (argc > 4)

            textHeight = Draw::Atoi(argv[4]);

        if (argc > 5)

            position = (Aspect_TypeOfColorScalePosition)Draw::Atoi(argv[5]);

        if (argc > 7)

        {

            X = Draw::Atof(argv[6]);

            Y = Draw::Atof(argv[7]);
        }
    }

    Handle(V3d_View) curView = ViewerTest::CurrentView();

    if (curView.IsNull())

        return 1;

    Handle(Aspect_ColorScale) aCSV = curView->ColorScale();

    Handle(V3d_ColorScale) aCS = (Handle(V3d_ColorScale)::DownCast(aCSV));

    if (!aCS.IsNull())

    {

        aCS->SetPosition(X, Y);

        aCS->SetHeight(0.95);

        aCS->SetTextHeight(textHeight);

        aCS->SetRange(minRange, maxRange);

        aCS->SetNumberOfIntervals(numIntervals);

        aCS->SetLabelPosition(position);

        if (!curView->ColorScaleIsDisplayed())

            curView->ColorScaleDisplay();
    }

    return 0;
}