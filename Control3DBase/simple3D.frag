//varying vec4 v_color;
uniform vec4 u_global_ambiance;

uniform vec4 u_light_diffuse[10];
uniform vec4 u_light_ambient[10];
uniform vec4 u_light_specular[10];
uniform float u_light_reach[10];

uniform float u_light_count_frag;

uniform vec4 u_material_diffuse;
uniform vec4 u_material_ambient;
uniform vec4 u_material_specular;
uniform float u_material_shiny;

varying vec4 v_normal;
varying vec4 v_s;
varying vec4 v_h;


void main(void)
{
    //Light 1
    vec4 light;

    for(int i = 0 ; i<u_light_count_frag;i++){
        float light_intesity =1.0;
        if (u_light_reach[i] != 0){
            float distance = length(v_s);
            if( distance > u_light_reach[i]){
                light_intesity = 0;
            }
            else {
                light_intesity =1- distance/ u_light_reach[i];
            }
        }

        float lambert = 0.0;
        float phong = 0.0;

        lambert = max(0.0,dot(v_normal, v_s)/(length(v_normal)*length(v_s)));

        phong =  max(0.0,dot(normalize(v_normal), normalize(v_h)));

        phong = pow(phong, u_material_shiny);

        light = light+(u_light_ambient[i] * u_material_ambient + lambert * u_light_diffuse[i] * u_material_diffuse + u_light_specular[i] * u_material_specular * phong)* light_intesity;
    };
    
    //all together
	
    gl_FragColor = u_global_ambiance*u_material_ambient + light;
}