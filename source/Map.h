#pragma once

#include "Graphics/Texture2D.h"
#include "Graphics/Mesh.hpp"
#include "Graphics/Shader.h" 
#include "Graphics/Font.h"
#include "Graphics/Quad.h"

#include <glm/vec2.hpp>
#include <glm/mat4x4.hpp>

#include <switch.h>

#include "Data.h"

template <typename T> class MapObject;

class MapLocation;
class Legend;
class Dialog;
class LineRenderer;
class KorokDialog;

namespace Map
{
    void Init();

    void UpdateMapObjects(int layer);

    void Update();
    void Render();

    bool IsInView(glm::vec2 position, float margin);

    void Destory();
    void SwitchLayer(int layer);
    const float m_DefaultZoom = 0.125f * 2;
    const float m_CameraWidth = 1280.0f;
    const float m_CameraHeight = 720.0f;
    const float m_ScreenLeft = -m_CameraWidth / 2.0f;
    const float m_ScreenRight = m_CameraWidth / 2.0f;
    const float m_ScreenTop = m_CameraHeight / 2.0f;
    const float m_ScreenBottom = -m_CameraHeight / 2.0f;
    extern int m_layer;
    extern TexturedQuad m_MapBackground;

    extern Font m_Font;
    extern LineRenderer* m_LineRenderer;

    extern TexturedQuad m_MasterModeIcon; 

    extern float m_Zoom;

    extern glm::mat4 m_ProjectionMatrix;
    extern glm::mat4 m_ViewMatrix;

    extern glm::vec2 m_CameraPosition;
    extern glm::vec2 m_PrevCameraPosition;

    extern int m_PrevTouchCount;
    extern glm::vec2 m_PrevTouchPosition;
    extern glm::vec2 m_StartDragPos;
    extern bool m_IsDragging;
    extern bool m_ShouldExit;
    extern bool m_LoadMasterMode;

    extern PadState* m_Pad;

    extern MapObject<Data::Korok>* m_Koroks;
    extern MapObject<Data::Shrine>* m_Shrines;
    extern MapObject<Data::DLCShrine>* m_DLCShrines;
    extern MapObject<Data::Hinox>* m_Hinoxes;
    extern MapObject<Data::Talus>* m_Taluses;
    extern MapObject<Data::Molduga>* m_Moldugas;
    extern MapObject<Data::Gleeok>* m_Gleeoks;
    extern MapObject<Data::Frox>* m_Froxes;
    extern MapObject<Data::FluxConstruct>* m_FluxConstructs;
    extern MapObject<Data::Cave>* m_Caves;
    extern MapObject<Data::Well>* m_Wells;
    extern MapObject<Data::Lightroot>* m_Lightroots;
    extern MapObject<Data::Chasm>* m_Chasms;
    extern MapLocation* m_Locations;

    extern Legend* m_Legend;
    extern KorokDialog* m_KorokDialog;
    extern Dialog* m_NoSavefileDialog;
    extern Dialog* m_GameRunningDialog;
    extern Dialog* m_MasterModeDialog;
};