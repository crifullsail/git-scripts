'''
import sculpt_falloff_switcher
sculpt_falloff_switcher.show()
'''
import maya.cmds as cmds


def show():
    window_name = "sculptFalloffSwitcherWindow"

    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name)

    def set_falloff(value):
        # Get the currently active Maya tool context.
        active_context = cmds.currentCtx()

        try:
            # Verify that the active context is a sculpting context.
            cmds.sculptMeshCacheCtx(
                active_context,
                query=True,
                falloffType=True
            )

            # Change the falloff type.
            cmds.sculptMeshCacheCtx(
                active_context,
                edit=True,
                falloffType=value
            )

            cmds.text(
                "falloffStatus",
                edit=True,
                label="Current Mode: " +
                ("Surface" if value == 1 else "Volume")
            )

        except RuntimeError:
            cmds.warning(
                "Please activate a Sculpting Tool first."
            )

    cmds.window(
        window_name,
        title="Sculpt Falloff Switcher",
        sizeable=False,
        widthHeight=(230, 85)
    )

    cmds.columnLayout(
        adjustableColumn=True,
        rowSpacing=8,
        columnOffset=("both", 8)
    )

    cmds.rowLayout(
        numberOfColumns=2,
        adjustableColumn=1,
        columnWidth2=(105, 105),
        columnAttach=[(1, "both", 2), (2, "both", 2)]
    )

    cmds.button(
        label="Surface",
        height=35,
        command=lambda *_: set_falloff(1)
    )

    cmds.button(
        label="Volume",
        height=35,
        command=lambda *_: set_falloff(2)
    )

    cmds.setParent("..")

    cmds.text(
        "falloffStatus",
        label="Select a falloff mode",
        height=25
    )

    cmds.showWindow(window_name)
