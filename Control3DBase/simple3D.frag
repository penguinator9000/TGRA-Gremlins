attribute vec4 a_position;
attribute vec4 a_normal;

uniform mat4 u_model_matrix;
uniform mat4 u_view_matrix;
uniform mat4 u_projection_matrix;

//uniform vec4 u_color;
uniform vec4 u_light_position;
uniform vec4 u_light_diffuse;
uniform vec4 u_light_ambient;
uniform vec4 u_light_specular;

uniform vec4 u_material_diffuse;
uniform vec4 u_material_ambient;
uniform vec4 u_material_specular;
uniform float u_material_shiny;

uniform vec4 u_eye_position;

varying vec4 v_color;

void main(void)
{
    vec4 position = vec4(a_position.x, a_position.y, a_position.z, 1.0);
	vec4 normal = vec4(a_normal.x, a_normal.y, a_normal.z, 0.0);
    vec4 s = vec4(0);
	vec4 v = vec4(0);
	vec4 h = vec4(0);
	float lambert = 0.0;
	float phong = 0.0;

    position = u_model_matrix * position;
	normal = u_model_matrix * normal;
	
	s = u_light_position - position;
	float distance = length(s);
	v = u_eye_position-position;
	h = (s+v);
	//lambert = max(0.0,dot(normalize(normal), normalize(s))); 
	lambert = max(0.0,dot(normal, s)/(length(normal)*length(s)));

	//phong =  max(0.0,dot(normalize(normal), normalize(h)));
	phong = max(0,dot(normal,h)/(length(normal)*length(h)));

	phong = pow(phong, u_material_shiny);
    v_color = u_light_ambient * u_material_ambient + (lambert * u_light_diffuse * u_material_diffuse + u_light_specular * u_material_specular * phong);

    gl_FragColor = v_color;
}