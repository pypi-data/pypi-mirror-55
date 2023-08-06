depends = ('ITKPyBase', 'ITKMesh', 'ITKImageGradient', 'ITKImageFunction', 'ITKCommon', )
templates = (
  ('CuberilleImageToMeshFilter', 'itk::CuberilleImageToMeshFilter', 'itkCuberilleImageToMeshFilterISS2MSS2', True, 'itk::Image< signed short,2 >, itk::Mesh< signed short,2 >'),
  ('CuberilleImageToMeshFilter', 'itk::CuberilleImageToMeshFilter', 'itkCuberilleImageToMeshFilterIUC2MUC2', True, 'itk::Image< unsigned char,2 >, itk::Mesh< unsigned char,2 >'),
  ('CuberilleImageToMeshFilter', 'itk::CuberilleImageToMeshFilter', 'itkCuberilleImageToMeshFilterIUS2MUS2', True, 'itk::Image< unsigned short,2 >, itk::Mesh< unsigned short,2 >'),
  ('CuberilleImageToMeshFilter', 'itk::CuberilleImageToMeshFilter', 'itkCuberilleImageToMeshFilterIF2MF2', True, 'itk::Image< float,2 >, itk::Mesh< float,2 >'),
  ('CuberilleImageToMeshFilter', 'itk::CuberilleImageToMeshFilter', 'itkCuberilleImageToMeshFilterISS3MSS3', True, 'itk::Image< signed short,3 >, itk::Mesh< signed short,3 >'),
  ('CuberilleImageToMeshFilter', 'itk::CuberilleImageToMeshFilter', 'itkCuberilleImageToMeshFilterIUC3MUC3', True, 'itk::Image< unsigned char,3 >, itk::Mesh< unsigned char,3 >'),
  ('CuberilleImageToMeshFilter', 'itk::CuberilleImageToMeshFilter', 'itkCuberilleImageToMeshFilterIUS3MUS3', True, 'itk::Image< unsigned short,3 >, itk::Mesh< unsigned short,3 >'),
  ('CuberilleImageToMeshFilter', 'itk::CuberilleImageToMeshFilter', 'itkCuberilleImageToMeshFilterIF3MF3', True, 'itk::Image< float,3 >, itk::Mesh< float,3 >'),
)
snake_case_functions = ('image_to_mesh_filter', 'cuberille_image_to_mesh_filter', 'mesh_source', )
