"""
Handle(AIS_Shape) aShapePrs = new AIS_Shape (theShape);
myIntContext->Display (aShapePrs, AIS_Shaded, 0, false, aShapePrs->AcceptShapeDecomposition());
myIntContext->SetColor(aShapePrs, Quantity_NOC_RED);

Handle(AIS_Shape) aShapePrs = new AIS_Shape (theShape);
aShapePrs->SetColor (Quantity_NOC_RED);
aShapePrs->SetDisplayMode (AIS_Shaded);
myIntContext->Display (aShapePrs);

AIS_ColoredShape aColoredShape = new AIS_ColoredShape (theShape);
// setup color of entire shape
aColoredShape->SetColor (Quantity_NOC_RED);
// setup line width of entire shape
aColoredShape->SetWidth (1.0);
// set transparency value
aColoredShape->SetTransparency (0.5);
// customize color of specified sub-shape
aColoredShape->SetCustomColor (theSubShape, Quantity_NOC_BLUE1);
// customize line width of specified sub-shape
aColoredShape->SetCustomWidth (theSubShape, 0.25);

Handle(Graphic3d_ArrayOfPoints) aPoints = new Graphic3d_ArrayOfPoints (2000, Standard_True);
aPoints->AddVertex (gp_Pnt(-40.0, -40.0, -40.0), Quantity_Color (Quantity_NOC_BLUE1));
aPoints->AddVertex (gp_Pnt (40.0,  40.0,  40.0), Quantity_Color (Quantity_NOC_BLUE2));
Handle(AIS_PointCloud) aPntCloud = new AIS_PointCloud();
aPntCloud->SetPoints (aPoints);

// read the data and create a data source
Handle(Poly_Triangulation) aSTLMesh = RWStl::ReadFile (aFileName);
Handle(XSDRAWSTLVRML_DataSource) aDataSource = new XSDRAWSTLVRML_DataSource (aSTLMesh);
// create mesh
Handle(MeshVS_Mesh) aMeshPrs = new MeshVS();
aMeshPrs->SetDataSource (aDataSource);
// use default presentation builder
Handle(MeshVS_MeshPrsBuilder) aBuilder = new MeshVS_MeshPrsBuilder (aMeshPrs);
aMeshPrs->AddBuilder (aBuilder, true);
"""